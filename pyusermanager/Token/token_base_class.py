from abc import ABC, abstractmethod
from pony.orm import db_session
import bcrypt
from pyusermanager import PyUserExceptions

###########################
#
# abstract Token class
#
###########################
class Token(ABC):
    def __init__(self, token=None):
        if token is not None:
            self.token = token
        else:
            self.token = None

    @abstractmethod
    def verify(self, ip):
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
        work_dict = {**type(self).__dict__,**self.__dict__}
        returnstring = f"\n--------{self.__class__.__name__}--------\n"
        #print(work_dict)
        for key,val in work_dict.items():
            if not key.startswith("_"):
                reee = f"{''.ljust(10-len(key),' ')}{key}: {val}\n"
                returnstring += reee
            
        return returnstring

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None

    def hash(self, to_hash):
        salt = bcrypt.gensalt()
        token_hash = bcrypt.hashpw(to_hash.encode("utf-8"), salt)
        self.token = token_hash.hex()
