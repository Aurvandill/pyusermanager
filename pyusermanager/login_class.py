from abc import ABC, abstractmethod
from pony.orm import *
import bcrypt


from pyusermanager import LdapStuff
from pyusermanager import AUTH_TYPE
from pyusermanager import UserFunctions
from pyusermanager import PyUserExceptions


class LoginHandler(ABC):
    def __init__(self, config, username, password):
        self.username = username
        self.password = password
        self.config = config

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
    def __init__(self, config, username, password):
        if username.endswith(self.config.suffix):
            username = username[: -len(self.config.suffix)]
            self.config = config
            super().__init__(username, password)
        else:
            raise PyUserExceptions.NotAnADUser

    def perform_login(self):
        ldap_auth = LdapStuff(self.config)

        if ldap_auth.login(self.username, self.password):
            return True
        else:
            return False


class LOCALLogin(LoginHandler):
    def perform_login(self):
        with db_session:
            requested_user = self.config.db.User.get(username=self.username)
            salt = requested_user.password_salt
            new_hash = bcrypt.hashpw(self.password.encode("utf-8"), salt)

            return new_hash == requested_user.password_hash


def login(config, username, password):

    with db_session:
        found_user = config.db.User.get(username=username)

        # if user does not exist
        if found_user is None:
            handle_login_missing(config, username, password)

        if found_user.auth_type == AUTH_TYPE.LOCAL:
            return LOCALLogin(config, username, password).perform_login()

        elif found_user.auth_type == AUTH_TYPE.AD and config.adcfg.login:
            return ADLogin(config, username, password, config.adcfg).perform_login()

        else:
            raise NotImplementedError


def handle_login_missing(config, username, password):
    Adconfig = config.adcfg
    if Adconfig.login:
        # perform ldap login
        if ADLogin(username, password, Adconfig).perform_login():
            # if successfull ad login create user in local db
            userfunc = UserFunctions(username, AUTH_TYPE.AD)

            userfunc.create(activated=True)
            return True
        else:
            raise PyUserExceptions.MissingUserException
    else:
        raise PyUserExceptions.MissingUserException
