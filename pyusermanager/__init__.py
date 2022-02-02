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
    - db_providers -> db provider ocnfigs (all db types supported by ponyorm)
        - DB_Provider (abstract Class)
        - CockroachDB_Provider
        - MYSQL_Provider
        - Oracle_Provider
        - PostgreSQL_Provider

"""

from pyusermanager import custom_exceptions as PyUserExceptions
from pyusermanager.auth_type_enum import *
from pyusermanager.data_classes import define_entitys as DefineEntitys
from pyusermanager import Config

from pyusermanager.ldap_stuff import LdapStuff
from pyusermanager.user_funcs import user
from pyusermanager.login_class import login

from pyusermanager.perms_class import Perm


from pyusermanager import Token


