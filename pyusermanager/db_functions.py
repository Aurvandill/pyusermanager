# Imports
from pony.orm import *
import bcrypt
from email.utils import parseaddr

from .config_class import LoginConfig
from .auth_type_enum import AUTH_TYPE

# db entries
from .data_classes import *

# configuration of ad module (default is deactivated)
from .ad_config_class import AD_Config

# custom exceptions!
from .custom_exceptions import (
    NotInitedException,
    MissingUserException,
    AlreadyExistsException,
    TokenMissingException,
)

# for ldap auth
from . import ldap_stuff


#######################
#
# User Stuff
#
#######################


def get_users():

    users_dict = {}

    with db_session:
        users = User.select()
        userlist = []
        for user in users:
            user_dict = {
                "username": user.username,
                "avatar": user.avatar,
                "activated": user.activated,
            }
            userlist.append(user_dict)

        # append userlist to dictionaries
        users_dict["users"] = userlist

    return users_dict




def update_password(username=None, password=""):

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    if type(password) != str or type(username) != str:
        raise TypeError("supplied Values not of correct Type")

    if len(password) <= LoginConfig.password_min_len:
        raise ValueError("password is to short!")

    with db_session:
        # check if user exists
        requested_user = User.get(username=username)
        if requested_user is None:
            raise MissingUserException("user to delete does not exist!")
        else:
            pw_salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)
            requested_user.password_hash = pw_hash
            requested_user.password_salt = pw_salt
            # invalidate login token
            logout_user(requested_user.token.token, force=True)
            # delete reset token if it exists!
            if requested_user.reset_code is not None:
                requested_user.reset_code.delete()


def get_extended_info(username, include_email=None):

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    with db_session:
        user = User.get(username=username)

        if user is None:
            # if we found no user return an empty dictionary
            raise MissingUserException("user you are looking for does not exist!")

        else:
            user_dict = {}
            user_dict["username"] = user.username
            user_dict["auth_type"] = user.auth_type.name
            user_dict["activated"] = user.activated
            user_dict["avatar"] = user.avatar
            if include_email is not None:
                user_dict["email"] = user.email

            token_dict = {}
            if user.token is not None:
                token_dict["last_login"] = str(user.token.last_login)
                token_dict["valid_until"] = str(user.token.valid_until)
                token_dict["valid_for"] = user.token.ip
                token_dict["token"] = user.token.token

            # add perms to dict!
            perm_dict = {}
            for perm in user.perms:
                perm_dict[perm.perm_name] = True

            return user_dict, token_dict, perm_dict


def set_avatar(username="", avatar_filename=""):

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    if type(username) != str or type(avatar_filename) != str:
        raise TypeError("supplied args not valid!")

    if "/" in avatar_filename:
        return ValueError("avatar filename contains illegal character!")

    with db_session:
        user = User.get(username=username)
        if user is None:
            raise MissingUserException("user does not exist!")
        else:
            user.avatar = avatar_filename

    return True


