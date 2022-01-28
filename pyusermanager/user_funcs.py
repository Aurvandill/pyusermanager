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

    def __str__(self):
        return f"""
--User Function Settings--
email_required:     {self.email_required}
password_min_len:   {self.password_min_len}
username_min_len:   {self.username_min_len}

        """

    def __init__(self,username,auth_type=AUTH_TYPE.LOCAL):

        if auth_type != AUTH_TYPE.AD and "@" in username:
            raise ValueError("@ in username is reserved for ad Users!")    
        self.username = username
        self.auth_type = AUTH_TYPE.LOCAL

    def verify_inputs(self, **kwargs):

        found_email = False
        for key, val in kwargs.items():
            # verify email if given
            if key == "email" and val == parseaddr(val)[1]:
                found_email = True
            # verify activated if gien
            if key == "activated" and not isinstance(val, bool):
                raise ValueError("Activates is not bool")

        if self.email_required and not found_email:
            raise ValueError("Email required but no valid provided!")

    def create(self, password=None, **kwargs):
        with db_session:
            try:
                dc.User[self.username]
                raise ce.AlreadyExistsException
            except ObjectNotFound as err:

                self.verify_inputs(**kwargs)

                if len(password) < self.password_min_len:
                    raise ValueError("password to short")

                if "@" in self.username and self.auth_type != AUTH_TYPE.AD:
                    raise ValueError(
                        "non ad users are not allowed to have @ in their name!"
                    )

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


    def change(self,**kwargs):

        if "email" in kwargs.items():
            self.changeemail(kwargs["email"])
        if "password" in kwargs.items():
            self.changepw(kwargs["password"])
        if "avatar" in kwargs.items():
            self.changeavatar(kwargs["avatar"])           

    def changepw(self,password):


        pass

    def changeemail(self,email):


        pass

    def changeavatar(self,avatar):

        with db_session:
            pass

        pass

    def hash_pw(self,password=None):
        if password is None:
            return None, None
        else:
            pw_salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)
            return pw_salt, pw_hash