from pony.orm import db_session
import datetime
from pyusermanager import PyUserExceptions
from .token_base_class import Token


class Auth(Token):
    """For Auth Tokens"""

    def __init__(self, config, token=None, username=None):
        self.config = config
        self.type = config.db.Auth_Token
        super().__init__(token, username)

    def invalidate(self, ip="127.0.0.1", force=False):
        with db_session:
            found_token = self.config.db.Auth_Token.get(token=self.token)

            if found_token is None:
                raise PyUserExceptions.TokenMissingException("could not find requested Token")

            if found_token.ip == ip or force:
                found_token.valid_until = "1999-01-01"
                return True
            else:
                return ValueError("ip differs -> not invalidating Token")

    def verify(self, ip):
        with db_session:
            try:
                found_token = self.type.get(token=self.token)
                now = datetime.datetime.now()
                valid_until = found_token.valid_until
                user = found_token.user

                if ip == user.token.ip and now <= valid_until:
                    self.username = user.username
                    return True
                return False
            # no token given or no token found
            except (ValueError, AttributeError):
                return False

    def create(self, ip=None, valid_days=1):
        valid_until = datetime.datetime.now() + datetime.timedelta(days=valid_days)
        token_to_hash = f"{self.username}@{ip};valid_until:{str(valid_until)}"
        super().hash(token_to_hash)

        with db_session:
            try:
                found_user = self.config.db.User[self.username]
            except Exception:
                raise PyUserExceptions.MissingUserException

            token = self.config.db.Auth_Token.get(user=self.username)

            # create new token if no token exists
            if token is None:
                self.config.db.Auth_Token(
                    user=found_user.username,
                    token=self.token,
                    ip=ip,
                    valid_until=valid_until,
                )

            # if token exists update it
            else:
                token.token = self.token
                token.valid_until = valid_until
                token.last_login = datetime.datetime.now()

            return True
