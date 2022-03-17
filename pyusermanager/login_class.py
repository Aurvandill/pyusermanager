from abc import ABC, abstractmethod
from pony.orm import *
import bcrypt


from pyusermanager import LdapStuff
from pyusermanager import AUTH_TYPE
from pyusermanager import user
from pyusermanager import PyUserExceptions
from pyusermanager import Perm


class LoginHandler(ABC):
    """An abstract Class
    says every class inehreting from this must implement perform_login
    """
    def __init__(self, config, username:str, password:str):
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

    def __init__(self, config, username:str, password:str):
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

    def get_special_groups(self):
        """gets all groups starting with the AD Prefix

        Returns:
            Array: List of all Groups
        """

        returned_groups = []
        if self.config.adcfg.groups_prefix is None:
            return returned_groups

        ldap_auth = LdapStuff(self.config.adcfg)

        groups = ldap_auth.get_ldap_groups(self.username,self.password)

        for group in groups:
            if group.startswith(self.config.adcfg.groups_prefix):
                returned_groups.append(group[len(self.config.adcfg.groups_prefix):])

        return returned_groups

    def update_groups(self):

        perms = Perm(self.config).get_all()

        print(perms)
        #remove all groups
        for perm in perms:
            Perm(self.config,perm).remove_from_user(f"{self.username}{self.config.adcfg.suffix}")
        
        #assign groups from ad (and create them if they are not existing)
        for perm in self.get_special_groups():
            tmp_perm = Perm(self.config,perm)
            tmp_perm.create()
            tmp_perm.assign_to_user(f"{self.username}{self.config.adcfg.suffix}")

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


def login(config, username:str, password:str):
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

    with db_session:
        found_user = config.db.User.get(username=username)

        # if user does not exist
        if found_user is None:
            return handle_login_missing(config, username, password)

        if found_user.auth_type == AUTH_TYPE.LOCAL:
            return LOCALLogin(config, username, password).perform_login()

        elif found_user.auth_type == AUTH_TYPE.AD:
            if not config.adcfg.login:
                raise PyUserExceptions.ADLoginProhibited
            
            ad_user = ADLogin(config, username, password)
            
            if ad_user.perform_login():
                ad_user.update_groups()
                return True

        return False


def handle_login_missing(config, username:str, password:str):
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

    if config.adcfg.login:
        # perform ldap login
        ad_user = ADLogin(config, username, password)
        if ad_user.perform_login():
            # if successfull ad login create user in local db
            userfunc = user(config = config, username = username, auth_type = AUTH_TYPE.AD)
            userfunc.create(activated=True)
            ad_user.update_groups()

            return True

    raise PyUserExceptions.MissingUserException
