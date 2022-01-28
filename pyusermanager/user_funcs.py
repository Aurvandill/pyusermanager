from email.utils import parseaddr
from pony.orm import *


import bcrypt

from . import custom_exceptions as ce
from . import data_classes as dc
from .auth_type_enum import AUTH_TYPE


class UserFunctions:

    # default config

    email_required = False
    password_min_len = 4
    username_min_len = 4
    activated = not email_required

    def config(self):
        return f"""
--User Function Settings--
email_required:     {self.email_required}
password_min_len:   {self.password_min_len}
username_min_len:   {self.username_min_len}

        """

    def __str__(self):
        if len(self.__dict__) > 0:
            return str(self.__dict__)
        return None

    def __init__(self, username=None, auth_type=AUTH_TYPE.LOCAL):
        if username is not None:
            self.verify_inputs(username=username)

        if auth_type != AUTH_TYPE.AD and "@" in str(username):
            raise ValueError("@ in username is reserved for ad Users!")
        self.username = str(username)
        self.auth_type = AUTH_TYPE.LOCAL

    """
    Gets all users including avatars
    retuns an array with a dictionary for each user
    example:
    [{"username": "admin","avatar":"admin.png"},{"username": "testuser","avatar":"default.png"}]
    """

    @staticmethod
    def get_users():
        userlist = []
        with db_session:
            users = dc.User.select()

            for user in users:
                user_dict = {
                    "username": user.username,
                    "avatar": user.avatar,
                }
                userlist.append(user_dict)

        return userlist

    @staticmethod
    def hash_pw(password=None):
        if password is None:
            return None, None
        else:
            pw_salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)
            return pw_salt, pw_hash

    def verify_inputs(self, **kwargs):

        found_email = False
        for key, val in kwargs.items():
            # verify email if given
            if key == "email" and val == parseaddr(val)[1]:
                found_email = True
            # verify activated if given
            if key == "activated" and not isinstance(val, bool):
                raise ValueError("Activated is not bool")
            # verify password if gien
            if key == "password" and len(val) < self.password_min_len:
                raise ValueError("password to short")
            # verify username if gien
            if key == "username" and (val == None or len(val) < self.username_min_len):
                raise ValueError("username to short")

        if self.email_required and not found_email:
            raise ValueError("Email required but no valid provided!")

    def create(self, password=None, **kwargs):
        with db_session:
            try:
                dc.User[self.username]
                raise ce.AlreadyExistsException
            except ObjectNotFound as err:

                self.verify_inputs(**kwargs, password=password)

                pw_salt, pw_hash = self.hash_pw(password)

                dc.User(
                    username=self.username,
                    password_hash=pw_hash,
                    password_salt=pw_salt,
                    auth_type=self.auth_type,
                    **kwargs,
                )
                return True

    def delete(self):

        with db_session:
            # check if user exists
            requested_user = dc.User.get(username=self.username)
            if requested_user is None:
                raise ce.MissingUserException("user to delete does not exist!")
            else:
                requested_user.delete()
                return True

    def check(self):
        with db_session:
            # check if user exists
            requested_user = dc.User.get(username=self.username)
            if requested_user is None:
                return False
            else:
                return True

    def change(self, **kwargs):

        if "email" in kwargs.items():
            self.changeemail(kwargs["email"])
        if "password" in kwargs.items():
            self.changepw(kwargs["password"])
        if "avatar" in kwargs.items():
            self.changeavatar(kwargs["avatar"])

    def changepw(self, password):
        if password is None:
            raise ValueError("password empty!")

        self.verify_inputs(password=password)

        with db_session:
            try:
                user = dc.User(self.username)
                pw_salt, pw_hash = self.hash_pw(password)
                user.password_salt = pw_salt
                user.password_hash = pw_hash
                return True
            except ObjectNotFound:
                raise ce.MissingUserException

    def changeemail(self, email):
        if email is None:
            raise ValueError("email is empty!")

        self.verify_inputs(email=email)

        with db_session:
            try:
                user = dc.User(self.username)
                user.email = email
                return True
            except ObjectNotFound:
                raise ce.MissingUserException

    def changeavatar(self, avatar):
        if avatar is None:
            raise ValueError("avatar name is invalid!")

        with db_session:
            try:
                user = dc.User(self.username)
                user.avatar = avatar
                return True
            except ObjectNotFound:
                raise ce.MissingUserException

    def info(self):
        with db_session:
            try:
                user = dc.User(self.username)

                return {
                    "username": user.username,
                }
            except ObjectNotFound:
                raise ce.MissingUserException
