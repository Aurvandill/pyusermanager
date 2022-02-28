from pony.orm import PrimaryKey, Optional, Required, Set
import datetime

from pyusermanager import AUTH_TYPE


def define_entitys(db):
    """
    This Functions registers db entitys to the database
    the Datatypes should be self explaining
    """
    class User(db.Entity):
        username = PrimaryKey(str)
        password_hash = Optional(bytes)
        auth_type = Required(AUTH_TYPE)
        email = Required(str, default="Invalid")
        avatar = Required(str, default="default.png")
        activated = Required(bool, default=False)
        token = Optional("Auth_Token", cascade_delete=True)
        perms = Set("Permissions")
        reset_code = Optional("ResetCode", cascade_delete=True)
        activation_code = Optional("ActivationCode", cascade_delete=True)

    class Auth_Token(db.Entity):
        user = PrimaryKey(User)
        token = Required(str)
        ip = Required(str)
        valid_until = Required(datetime.datetime, default=datetime.datetime.utcnow)
        last_login = Required(datetime.datetime, default=datetime.datetime.utcnow)

    class Permissions(db.Entity):
        perm_name = PrimaryKey(str)
        user_reference = Set(User)

    # passwort-Reset Table containg hashes
    class ResetCode(db.Entity):
        user = PrimaryKey(User)
        token = Required(str)
        valid_until = Required(datetime.datetime, default=datetime.datetime.utcnow)

    # activation-table contains hashes send to users to activate their accounts!
    class ActivationCode(db.Entity):
        user = PrimaryKey(User)
        token = Required(str)
        valid_until = Required(datetime.datetime, default=datetime.datetime.utcnow)
