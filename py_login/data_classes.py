from pony.orm import *
import datetime
from auth_type_enum import AUTH_TYPE

from config_class import LoginConfig

class User(LoginConfig.db.Entity):
    username = PrimaryKey(str)
    password_hash = Optional(bytes)
    password_salt = Optional(bytes)
    auth_type = Required(AUTH_TYPE)

    if LoginConfig.email_required:
        email = Required(str)
    else:
        email = Optional(str)
    activated = Required(bool,default=LoginConfig.auto_activate_accounts)

    token = Optional('Auth_Token')
    perms = Set('Permissions')
    reset_code = Optional('ResetCode')
    activation_code = Optional('ActivationCode')
    

class Auth_Token(LoginConfig.db.Entity):
    user = PrimaryKey(User)
    token = Required(str)
    ip = Required(str)
    valid_until = Required(str)
    last_login = Required(datetime.datetime,default=datetime.datetime.utcnow)

class Permissions(LoginConfig.db.Entity):
    perm_name = PrimaryKey(str)
    user_reference = Set(User)

#passwort-Reset Table containg hashes
class ResetCode(LoginConfig.db.Entity):
    user = PrimaryKey(User)
    token = Required(str)
    valid_until = Required(datetime.datetime,default=datetime.datetime.utcnow)

#activation-table contains hashes send to users to activate their accounts!
class ActivationCode(LoginConfig.db.Entity):
    user = PrimaryKey(User)
    token = Required(str)
