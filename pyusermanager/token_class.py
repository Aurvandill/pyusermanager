from abc import ABC, abstractmethod
from enum import Enum
import datetime
import bcrypt

from pony.orm import *

from . import custom_exceptions as ce
from . import data_classes as dc

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
                raise ce.TokenMissingException

    def set_user(self, username):
        self.username = username

    def get_token(self):
        with db_session:
            try:
                self.token = self.type.get(user=self.username).token
            except AttributeError:
                raise ce.TokenMissingException

    def delete(self):
        with db_session:
            try:
                token = self.type.get(token=self.token).delete()
                return True
            except ValueError:
                raise ce.TokenMissingException

    def __str__(self):

        if len(self.__dict__) > 0:
            return str(self.__dict__)
        else:
            return None

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None

    def hash(self, to_hash):
        salt = bcrypt.gensalt()
        token_hash = bcrypt.hashpw(to_hash.encode("utf-8"), salt)
        self.token = token_hash.hex()


###########################
#
# Auth Token
#
###########################
class Auth(Token):
    def __init__(self, token=None):
        self.type = dc.Auth_Token
        super().__init__(token)

    def invalidate(self,ip = "127.0.0.1", force = False):
        with db_session:
            found_token = dc.Auth_Token.get(token=self.token)

            if found_token is None:
                raise ce.TokenMissingException("could not find requested Token")
            
            if found_token.ip == ip or force:
                found_token.valid_until = "1999-01-01"
                return True
            else:
                return ValueError("ip differs -> not invalidating Token")

    def verify(self, ip):
        with db_session:
            try:
                found_token = self.type.get(token=self.token)
                now = datetime.datetime.now()
                valid_until = found_token.valid_until
                user = found_token.user

                if ip == user.token.ip and now <= valid_until:
                    self.username = user.username
                    return True
                return False
            # no token given or no token found
            except (ValueError,AttributeError):
                return False

    def create(self, ip=None, valid_days=1):
        valid_until = datetime.datetime.now() + datetime.timedelta(days=valid_days)
        token_to_hash = f"{self.username}@{ip};valid_until:{str(valid_until)}"
        super().hash(token_to_hash)

        with db_session:
            try:
                found_user = dc.User.get(username=self.username)
            except Exception:
                raise ce.MissingUserException

            token = dc.Auth_Token.get(user=self.username)

            # create new token if no token exists
            if token is None:
                dc.Auth_Token(
                    user=found_user.username,
                    token=self.token,
                    ip=ip,
                    valid_until=valid_until,
                )

            # if token exists update it
            else:
                token.token = self.token
                token.valid_until = valid_until

            return True


###########################
#
# Activation Token
#
###########################
class Activation(Token):
    def __init__(self, token=None):
        self.type = dc.ActivationCode
        super().__init__(token)

    def verify(self, ip=None):
        with db_session:
            try:
                found_token = self.type.get(token=self.token)
                user = found_token.user
                user.activated = True
                found_token.delete()
                self.token = None
                self.username = user.username
                return True
            # no token given or no token found
            except (ValueError,AttributeError):
                return False

    def create(self):
        token_to_hash = f"{self.username}-activation"
        super().hash(token_to_hash)

        with db_session:
            try:
                found_user = dc.User.get(username=self.username)
            except Exception:
                raise ce.MissingUserException

            token = dc.ActivationCode.get(user=self.username)

            # create new token if no token exists
            if token is None:
                dc.ActivationCode(user=found_user.username, token=self.token)

            # if token exists update it
            else:
                token.token = self.token

            return True


###########################
#
# Reset Token
#
###########################
class Reset(Token):
    def __init__(self, token=None):
        self.type = dc.ResetCode
        super().__init__(token)

    def verify(self):
        with db_session:
            try:
                found_token = self.type.get(token=self.token)

                if found_token is None:
                    raise ce.TokenMissingException

                now = datetime.datetime.now()
                valid_until = found_token.valid_until
                user = found_token.user
                if now <= valid_until:
                    self.username = user.username
                    return True
                return False
            # no token given or no token found
            except (ValueError,AttributeError):
                return False

    def create(self):
        valid_until = datetime.datetime.now() + datetime.timedelta(days=1)
        token_to_hash = f"{self.username}-reset;valid_until:{str(valid_until)}"
        super().hash(token_to_hash)

        print(self)

        with db_session:
            try:
                found_user = dc.User.get(username=self.username)
            except Exception:
                raise ce.MissingUserException

            token = dc.ResetCode.get(user=self.username)

            # create new token if no token exists
            if token is None:
                dc.ResetCode(
                    user=found_user.username, token=self.token, valid_until=valid_until
                )
            # if token exists update it
            else:
                token.token = self.token
                token.valid_until = valid_until

            return True
