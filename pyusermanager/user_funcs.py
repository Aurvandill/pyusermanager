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

    def __init__(
        self, email_required=None, password_min_len=None, username_min_len=None
    ):
        if email_required is not None:
            self.email_required = email_required
        if password_min_len is not None:
            self.password_min_len = password_min_len
        if username_min_len is not None:
            self.username_min_len = username_min_len

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

    def CreateUser(self, username, password=None, auth_type=AUTH_TYPE.LOCAL, **kwargs):
        with db_session:
            try:
                dc.User[username]
                raise ce.AlreadyExistsException
            except ObjectNotFound as err:

                self.verify_inputs(**kwargs)

                if len(password) < self.password_min_len:
                    raise ValueError("password to short")

                if "@" in username and auth_type != AUTH_TYPE.AD:
                    raise ValueError(
                        "non ad users are not allowed to have @ in their name!"
                    )

                pw_salt, pw_hash = self.hash_pw(password)

                dc.User(
                    username=username,
                    password_hash=pw_hash,
                    password_salt=pw_salt,
                    auth_type=auth_type,
                    **kwargs,
                )
                return True

    def hash_pw(password=None):
        if password is None:
            return None, None
        else:
            pw_salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode("utf-8"), pw_salt)
            return pw_salt, pw_hash
