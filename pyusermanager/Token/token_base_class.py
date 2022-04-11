from abc import ABC, abstractmethod
from pony.orm import db_session
import bcrypt
from .. import custom_exceptions as PyUserExceptions
import datetime

###########################
#
# abstract Token class
#
###########################
class Token(ABC):
    """Abstract Token Base Class"""

    def __init__(self, token=None, username=None):

        self.token = token
        self.username = username

    @abstractmethod
    def verify(self, ip):
        pass

    @abstractmethod
    def create(self):
        pass

    def get_user(self):
        with db_session:
            try:
                self.username = self.type.get(token=self.token).user.username
                return True
            except Exception:
                raise PyUserExceptions.TokenMissingException

    def set_user(self, username):
        self.username = username

    def get_token(self):
        with db_session:
            try:
                self.token = self.type.get(user=self.username).token
            except AttributeError:
                raise PyUserExceptions.TokenMissingException

    def delete(self):
        with db_session:
            try:
                self.type.get(token=self.token).delete()
                return True
            except ValueError:
                raise PyUserExceptions.TokenMissingException

    def __str__(self):
        return f"""
--------{self.__class__.__name__}--------
username: {self.username}
   token: {self.token}        
"""

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None

    def hash(self, to_hash):
        salt = bcrypt.gensalt()
        token_hash = bcrypt.hashpw(to_hash.encode("utf-8"), salt)
        self.token = token_hash.hex()

    def set_lifetime(self, valid_days=1):
        with db_session:
            try:
                valid_until = datetime.datetime.now() + datetime.timedelta(days=valid_days)
                self.type.get(token=self.token).valid_until = valid_until
                return True
            except:
                return False
