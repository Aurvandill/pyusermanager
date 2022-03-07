from abc import ABC, abstractmethod
from pony.orm import *
import bcrypt


from pyusermanager import LdapStuff
from pyusermanager import AUTH_TYPE
from pyusermanager import user
from pyusermanager import PyUserExceptions


class LoginHandler(ABC):
    """An abstract Class
    says every class inehreting from this must implement perform_login
    """
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
    """LoginHandler for AD/LDAP Users"""

    def __init__(self, config, username, password):
        """removes ad suffix because the ldapstuff needs and suffix free username
        
        Parameters:
        config (AD_Config)
        username (str): username of user to login
        password (str): password of user to login
        
        Exceptions:
            PyUserExceptions.NotAnADUser -> if the requested username passed to init does not end with the specified ad suffix in AD_Config
        """
        if username.endswith(config.adcfg.suffix):
            username = username[: -len(config.adcfg.suffix)]
            super().__init__(config, username, password)
        else:
            raise PyUserExceptions.NotAnADUser

    def perform_login(self):
        """performs Login

        Returns:
            success (bool): was the login successfull?
        """

        ldap_auth = LdapStuff(self.config.adcfg)

        if ldap_auth.login(self.username, self.password):
            return True
        else:
            return False


class LOCALLogin(LoginHandler):
    """LoginHandler for Local Users"""

    def perform_login(self):
        """performs Login

        Returns:
            success (bool): was the login successfull?
        """
        with db_session:
            requested_user = self.config.db.User.get(username=self.username)
            pw_hash = requested_user.password_hash

            return bcrypt.checkpw(self.password.encode("utf-8"),pw_hash)


def login(config, username, password):
    """Login Function for calling from Other Function

    Parameters:
        config (General_Config): holds information for AD and misc.
        username (str): username of user to login
        password (str): password of user to login 

    Returns:
        success (bool): was the login successfull?

    Exceptions:
        PyUserExceptions.NotImplementedError if its handed a AUTH_TYPE which is not supported
        PyUserExceptions.MissingUserException
    """

    print(username)

    with db_session:
        found_user = config.db.User.get(username=username)

        # if user does not exist
        if found_user is None:
            return handle_login_missing(config, username, password)

        if found_user.auth_type == AUTH_TYPE.LOCAL:
            return LOCALLogin(config, username, password).perform_login()

        elif found_user.auth_type == AUTH_TYPE.AD and config.adcfg.login:
            return ADLogin(config, username, password).perform_login()

        else:
            raise NotImplementedError("logintype not supported")


def handle_login_missing(config, username, password):
    """Login Function for users not found in the db
    if its and AD/LDAP User it creates an entry in the db for that user

    Parameters:
        config (General_Config): holds information for AD and misc.
        username (str): username of user to login
        password (str): password of user to login 

    Returns:
        success (bool): was the login successfull?

    Exceptions:
        PyUserExceptions.MissingUserException
    """
    Adconfig = config.adcfg
    
    if Adconfig.login:
        # perform ldap login
        if ADLogin(config, username, password).perform_login():
            # if successfull ad login create user in local db
            userfunc = user(config = config, username = username, auth_type = AUTH_TYPE.AD)

            userfunc.create(activated=True)
            return True
        else:
            raise PyUserExceptions.MissingUserException
    else:
        raise PyUserExceptions.MissingUserException
