from email.utils import parseaddr
from pony.orm import *


import bcrypt

from pyusermanager import custom_exceptions as PyUserExceptions
from .auth_type_enum import AUTH_TYPE


class user:
    """
    A Class to manage Users in the Database
    """

    def __str__(self):
        if len(self.__dict__) > 0:
            return str(self.__dict__)
        return None

    def __init__(self, config, username=None, auth_type=AUTH_TYPE.LOCAL):
        """Function to init a User Object
        Parameters:
        cfg (General_Config): General Config Object used for stuff like simple Parameter Verification
        username (str): Username for the specified User
        auth_type (AUTH_TYPE enum): Specifies the User Type specified in the AUTH_TYPE enum

        """
        self.cfg = config
        if username is not None:
            self.verify_inputs(username=username)

        if auth_type != AUTH_TYPE.AD and "@" in str(username):
            raise ValueError("@ in username is reserved for ad Users!")
        self.username = str(username)
        self.auth_type = AUTH_TYPE.LOCAL

    def get_users(self):
        """
        Gets all users including avatars as an array filled with dictionarys

        Returns:
        List filled with dicts

        example:
        [{"username": "admin","avatar":"admin.png"},{"username": "testuser","avatar":"default.png"}]
        """
        userlist = []
        with db_session:
            users = self.cfg.db.User.select()

            for user in users:
                user_dict = {
                    "username": user.username,
                    "avatar": user.avatar,
                }
                userlist.append(user_dict)

        return userlist

    @staticmethod
    def hash_pw(password=None):
        """A Function to hash specified Password (or any other string)

        Parameters:
        password (str): a string which will get hashed

        Returns:
        byte: pw_salt (salt used to hash input)
        byte: pw_hash (hash of input)

        """
        if password is None:
            return None, None
        else:
            pw_salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)
            return pw_salt, pw_hash

    def verify_inputs(self, **kwargs):
        """A Function to check some qualitys of parameters

        Exceptions:
        ValueError -> if any parameter does not match requirements written down in the passed general config (self.cfg)
        """

        found_email = False
        if (
            "email" in kwargs
            and kwargs.get("email") == parseaddr(kwargs.get("email"))[1]
        ):
            found_email = True
        # verify activated if given
        if "activated" in kwargs and not isinstance(kwargs.get("activates"), bool):
            raise ValueError("Activated is not bool")
        # verify password if gien
        if (
            "password" in kwargs
            and len(kwargs.get("password")) < self.cfg.password_min_len
        ):
            raise ValueError("password to short")
        # verify username if gien
        if "username" in kwargs and (
            kwargs.get("username") == None
            or len(kwargs.get("username")) < self.cfg.username_min_len
        ):
            raise ValueError("username to short")

        if self.cfg.email_required and not found_email:
            raise ValueError("Email required but no valid provided!")

    def create(self, password=None, **kwargs):
        """A Function to create a User in the Database

        Parameters:
        password (str) mandatory
        self.auth_type (AUTH_TYPE) <- provided by object!
        email (str) optional
        avatar (str) optional (is a path to the avatar)
        activated (bool) if user is already activated

        Returns:
        success (bool) -> Usualy true since everythign else would raise an Exception

        Exceptions:
        PyUserExceptions.AlreadyExistsException -> if the user already exists
        ValueError -> if parameters do not pass according to verify_inputs
        """

        with db_session:
            try:
                self.cfg.db.User[self.username]
                raise PyUserExceptions.AlreadyExistsException
            except ObjectNotFound as err:

                self.verify_inputs(**kwargs, password=password)

                pw_salt, pw_hash = self.hash_pw(password)

                self.cfg.db.User(
                    username=self.username,
                    password_hash=pw_hash,
                    auth_type=self.auth_type,
                    **kwargs,
                )
                return True

    def delete(self):
        """A Function to delete a User in the Database

        Returns:
        success (bool) -> Usualy true since everythign else would raise an Exception

        Exceptions:
        PyUserExceptions.MissingUserException -> if user to delete does not exist!
        """
        with db_session:
            # check if user exists
            requested_user = self.cfg.db.User.get(username=self.username)
            if requested_user is None:
                raise PyUserExceptions.MissingUserException(
                    "user to delete does not exist!"
                )
            else:
                requested_user.delete()
                return True

    def check(self):
        """A Function to check if a user exists

        Returns:
        success (bool) -> true = user exists, false = user does not exist
        """
        with db_session:
            # check if user exists
            requested_user = self.cfg.db.User.get(username=self.username)
            if requested_user is None:
                return False
            else:
                return True

    def change(self, **kwargs):
        """A Function to change multiple user Attributes

        Parameters: (keyword params only!)
        password (str)
        email (str)
        avatar (str)

        Exceptions
        see changepw(), changeemail(), changeavatar()
        """

        if "email" in kwargs:
            self.changeemail(kwargs["email"])
        if "password" in kwargs:
            self.changepw(kwargs["password"])
        if "avatar" in kwargs:
            self.changeavatar(kwargs["avatar"])

    def changepw(self, password):
        """A Function to change the users password

        Parameters:
        password (str)

        Exceptions
        ValueError -> if password is to short or None
        """

        if password is None:
            raise ValueError("password empty!")

        self.verify_inputs(password=password)

        with db_session:
            try:
                user = self.cfg.db.User[self.username]
                pw_salt, pw_hash = self.hash_pw(password)
                user.password_hash = pw_hash
                return True
            except ObjectNotFound:
                raise PyUserExceptions.MissingUserException

    def changeemail(self, email):
        """A Function to change the users email

        Parameters:
        email (str)

        Exceptions
        ValueError -> if email is not "valid"
        """
        if email is None:
            raise ValueError("email is empty!")

        self.verify_inputs(email=email)

        with db_session:
            try:
                user = self.cfg.db.User[self.username]
                user.email = email
                return True
            except ObjectNotFound:
                raise PyUserExceptions.MissingUserException

    def changeavatar(self, avatar):
        """A Function to change the users avatar

        Parameters:
        avatar (str)

        Exceptions
        ValueError -> if avatar is None
        """
        if avatar is None:
            raise ValueError("avatar name is invalid!")

        with db_session:
            try:
                user = self.cfg.db.User[self.username]
                user.avatar = avatar
                return True
            except ObjectNotFound:
                raise PyUserExceptions.MissingUserException

    def info(self, include_email=False):
        """A Function to return a users public information

        Parameters:
        include_email (bool) -> if set to true the returned dictionary will include the email address of the user

        return:
        Dictionary with user information
        example:
        {"username":"admin", "avatar":"default.png", "activated":True, "email":"testemail@local"}

        Exceptions
        PyUserExceptions.MissingUserException -> if requested user is not found
        """
        with db_session:
            try:
                user = self.cfg.db.User[self.username]

                return_dict = {
                    "username": user.username,
                    "avatar": user.avatar,
                    "activated": user.activated,
                }
                if include_email:
                    return_dict["email"] = user.email

                return return_dict

            except ObjectNotFound:
                raise PyUserExceptions.MissingUserException

    def info_extended(self):
        """A Function to return userinfo + auth token info + perms

        return:
        Dictionary with user information
        example:
        {"username":"admin", "avatar":"default.png", "activated":True, "email":"testemail@local", token:{"last_login":"01.01.2022 13:37", "valid_until":"02.01.2022 13:37"....},"perms":["admin","testgroup"]}

        Exceptions
        PyUserExceptions.MissingUserException -> if requested user is not found
        """
        with db_session:
            try:
                user = self.cfg.db.User[self.username]
                return_dict = self.info(include_email=True)
                token_dict = {}
                if user.token is not None:
                    token_dict["last_login"] = str(user.token.last_login)
                    token_dict["valid_until"] = str(user.token.valid_until)
                    token_dict["valid_for"] = user.token.ip
                    token_dict["token"] = user.token.token
                # add perms to dict!
                perm_array = []
                for perm in user.perms:
                    perm_array.append(perm.perm_name)

                return_dict["token"] = token_dict
                return_dict["perms"] = perm_array

                return return_dict

            except ObjectNotFound:
                raise PyUserExceptions.MissingUserException
