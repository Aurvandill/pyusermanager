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

def logout_user(token="", ip="127.0.0.1", force=False):

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    with db_session:
        found_token = Auth_Token.get(token=token)

        if found_token is None:
            raise TokenMissingException("could not find requested Token")
        else:
            if found_token.ip == ip or force:
                found_token.valid_until = "1999-01-01"
                return True
            else:
                return ValueError("ip differs -> not invalidating Token")


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


def delete_user(username=None):
    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    with db_session:
        # check if user exists
        requested_user = User.get(username=username)
        if requested_user is None:
            raise MissingUserException("user to delete does not exist!")
        else:
            requested_user.delete()
            return True


def does_user_exist(user=None):

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    if user is None:
        return False
    with db_session:
        user = User.get(username=user)
        if user is None:
            # if we found no user return an empty dictionary
            return False
        else:
            return True


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

#######################
#
# Perm/Group Stuff
#
#######################


def create_perm(perm_name=None):

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    if type(perm_name) != str:
        raise TypeError("supplied args not valid!")

    # perm creation!

    with db_session:
        # check if perm exists
        perm = Permissions.get(perm_name=perm_name)

        if perm is not None:
            return False
        else:
            # create perm
            perm = Permissions(perm_name=perm_name)

    return True


def delete_perm(perm_name=None):
    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    if type(perm_name) != str:
        raise TypeError("supplied args not valid!")

    with db_session:
        # check if perm exists
        perm = Permissions.get(perm_name=perm_name)

        if perm is None:
            return False
        else:
            # delete perm
            perm.delete()

    return True


def assign_perm_to_user(username=None, perm=None):

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    if type(perm) != str or type(username) != str:
        raise ValueError("supplied parameters are invalid!")

    if username is None or len(username) < LoginConfig.username_min_len:
        raise ValueError("invalid Username supplied!")

    with db_session:
        user = User.get(username=username)
        if user is None:
            raise MissingUserException("User to assign Perms to does not exist!")
        else:
            found_perm = Permissions.get(perm_name=perm)
            if found_perm is not None:
                user.perms.add(found_perm)
                return True

    return False


def remove_perm_from_user(username=None, perm=None):
    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    if type(perm) != str or type(username) != str:
        raise ValueError("supplied parameters are invalid!")

    if username is None or len(username) < LoginConfig.username_min_len:
        raise ValueError("invalid Username supplied!")

    with db_session:
        user = User.get(username=username)
        if user is None:
            raise MissingUserException("User to assign Perms to does not exist!")
        else:
            # check if user has perm

            found_perm = Permissions.get(perm_name=perm)
            if found_perm is not None:
                user.perms.remove(found_perm)
                return True

    return False


def get_all_perms():

    if not LoginConfig.inited:
        raise NotInitedException("Config not inited!")

    perms = []

    with db_session:
        for perm in Permissions.select():
            perms.append(perm.perm_name)

    return perms
