"""
A Module used to manage Users in a database

Features:
- login users
- create Users

Modules:
- PyUserExceptions -> some Excpetions which get Thrown by this library
- LdapStuff -> a class to manage the LDAP/AD Login Process
- Perm -> used toi create perms and assign them to users
- login
    - LoginHandler (abstract class)
    - LOCALLogin (used to login Local Users)
    - ADLogin (used to log in AD Users)
- Token -> used to generate Tokens
    - Token (abstract class)
    - Activation
    - Reset
    - Auth
- Config -> for configuration of the library
    - AbstractConfig (abstract Class)
    - AD_Config
    - General_Config
    - db_providers -> db provider configs (all db types supported by ponyorm)
        - DB_Provider (abstract Class)
        - CockroachDB_Provider
        - MYSQL_Provider
        - Oracle_Provider
        - PostgreSQL_Provider

"""

from . import custom_exceptions as PyUserExceptions
from .auth_type_enum import *
from .data_classes import define_entitys as DefineEntitys
from .ldap_stuff import LdapStuff
from .user_funcs import user
from .perms_class import Perm
from .login_class import login
from ._version import __version__
from .authprovider_class import AuthProvider


