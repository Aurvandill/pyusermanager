from abc import ABC, abstractmethod
from enum import Enum
import datetime

from pony.orm import *

from . import data_classes as dc

class Token(ABC):

    def __init__(self,token=None):
        if token is not None:
            self.token = token
        else:
            self.token = None

    @abstractmethod
    def verify(self,ip):
        pass

    def get(self,username):
        with db_session:
            try:
                self.token = self.type.get(user = username).token
            except AttributeError:
                self.token = None

    def delete(self):
        with db_session:
            try:
                self.type.get(token = self.token).delete()
                return True
            #no token given!
            except ValueError:
                return False
            #no token found
            except AttributeError:
                return True

    def __str__(self):
        
        if len(self.__dict__) > 0:
            return_string = f"_________{self.__class__.__name__}_________\n\n"
            for key, value in self.__dict__.items():
                return_string += f"{key}:\t{value}\n"
            return_string += f"___________________________________________\n"
            return return_string
        else:
            return None

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None



class Auth(Token):

    def __init__(self,token=None):
        self.type = dc.Auth_Token
        super().__init__(token)

    def verify(self,ip):
        with db_session:
            try:
                found_token=self.type.get(token=self.token)
                now = datetime.datetime.now()
                valid_until = found_token.valid_until
                user = found_token.user

                if ip == user.token.ip and now <= valid_until:
                    self.related_user = user.username
                    return True
                else:
                    return False
            #no token given!
            except ValueError:
                return False
            #no token found
            except AttributeError:
                return True 


class Activation(Token):

    def __init__(self,token=None):
        self.type = dc.ActivationCode
        super().__init__(token)

    def verify(self,ip=None):
        with db_session:
            try:
                found_token = self.type.get(token=self.token)
                user = found_token.user
                user.activated = True
                found_token.delete()
                self.token = None
                self.related_user = user.username
                return True
            #no token given!
            except ValueError:
                return False
            #no token found
            except AttributeError:
                return True


class Reset(Token):

    def __init__(self,token=None):
        self.type = dc.ResetCode
        super().__init__(token)

    def verify(self,ip=None):
        with db_session:
            try:
                found_token=self.type.get(token=self.token)
                now = datetime.datetime.now()
                valid_until = found_token.valid_until
                user = found_token.user
                if now <= valid_until:
                    self.related_user = user.username
                    return True
                else:
                    return False
            #no token given!
            except ValueError:
                return False
            #no token found
            except AttributeError:
                return True
