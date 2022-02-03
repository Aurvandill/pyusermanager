from pony.orm import db_session
from pyusermanager import PyUserExceptions
from .token_base_class import Token

import datetime


###########################
#
# Reset Token
#
###########################
class Reset(Token):
    """For Reset Tokens"""
    def __init__(self, config, token=None, username=None):
        self.config = config
        self.type = self.config.db.ResetCode
        super().__init__(token, username)

    def verify(self):
        with db_session:
            try:
                found_token = self.type.get(token=self.token)

                if found_token is None:
                    raise PyUserExceptions.TokenMissingException

                now = datetime.datetime.now()
                valid_until = found_token.valid_until
                user = found_token.user
                if now <= valid_until:
                    self.username = user.username
                    return True
                return False
            # no token given or no token found
            except (ValueError, AttributeError):
                return False

    def create(self):
        valid_until = datetime.datetime.now() + datetime.timedelta(days=1)
        token_to_hash = f"{self.username}-reset;valid_until:{str(valid_until)}"
        super().hash(token_to_hash)

        print(self)

        with db_session:
            try:
                found_user = self.config.db.User.get(username=self.username)
            except Exception:
                raise PyUserExceptions.MissingUserException

            token = self.config.db.ResetCode.get(user=self.username)

            # create new token if no token exists
            if token is None:
                self.config.db.ResetCode(
                    user=found_user.username, token=self.token, valid_until=valid_until
                )
            # if token exists update it
            else:
                token.token = self.token
                token.valid_until = valid_until

            return True
