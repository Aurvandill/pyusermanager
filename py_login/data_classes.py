from pony.orm import *
import datetime
from auth_type_enum import AUTH_TYPE

from config_class import LoginConfig

class User(LoginConfig.db.Entity):
    username = PrimaryKey(str)
    password_hash = Optional(bytes)
    password_salt = Optional(bytes)
    auth_type = Required(AUTH_TYPE)
    token = Optional('Auth_Token')
    perms = Set('Permissions')

class Auth_Token(LoginConfig.db.Entity):
    user = PrimaryKey(User)
    token = Required(str)
    ip = Required(str)
    valid_until = Required(str)
    last_login = Required(datetime.datetime,default=datetime.datetime.utcnow)

class Permissions(LoginConfig.db.Entity):
    perm_name = PrimaryKey(str)
    user_reference = Set(User)
