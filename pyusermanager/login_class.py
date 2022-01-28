from abc import ABC, abstractmethod
from .ldap_stuff import LdapStuff

from pony.orm import *

import bcrypt

from . import custom_exceptions as ce
from . import data_classes as dc

from .ad_config_class import AD_Config
from .auth_type_enum import AUTH_TYPE
from .user_funcs import UserFunctions


class LoginHandler(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abstractmethod
    def perform_login():
        pass

    def __str__(self):

        if len(self.__dict__) > 0:
            return self.__dict__
        else:
            return None

    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None


class ADLogin(LoginHandler):
    def __init__(self, username, password, config):
        if username.endswith(self.config.suffix):
            username = username[: -len(self.config.suffix)]
            self.config = config
            super().__init__(username, password)
        else:
            raise ce.NotAnADUser

    def perform_login(self):
        ldap_auth = LdapStuff(self.config)

        if ldap_auth.login(self.username, self.password):
            return True
        else:
            return False


class LOCALLogin(LoginHandler):
    def perform_login(self):
        with db_session:
            requested_user = dc.User.get(username=self.username)
            salt = requested_user.password_salt
            new_hash = bcrypt.hashpw(self.password.encode("utf-8"), salt)

            return new_hash == requested_user.password_hash


def Login(username, password, Adconfig=AD_Config(False)):

    with db_session:
        found_user = dc.User.get(username=username)

        # if user does not exist
        if found_user is None:
            handle_login_missing(username, password, Adconfig)

        if found_user.auth_type == AUTH_TYPE.LOCAL:
            return LOCALLogin(username, password).perform_login()

        elif found_user.auth_type == AUTH_TYPE.AD and AD_Config.login:
            return ADLogin(username, password, Adconfig).perform_login()

        else:
            raise NotImplementedError

def handle_login_missing(username, password, Adconfig):
    if Adconfig.login:
        # perform ldap login
        if ADLogin(username, password, Adconfig).perform_login():
            #if successfull ad login create user in local db
            UserFunctions(False).create(
                username=username, auth_type=AUTH_TYPE.AD, activated=True
            )
            return True
        else:
            raise ce.MissingUserException
    else:
        raise ce.MissingUserException