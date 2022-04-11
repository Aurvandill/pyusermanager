from pony.orm import db_session
from .. import custom_exceptions as PyUserExceptions
from .token_base_class import Token
import datetime

###########################
#
# Activation Token
#
###########################
class Activation(Token):
    """For Activation Tokens"""

    def __init__(self, config, token=None, username=None):
        self.config = config
        self.type = self.config.db.ActivationCode
        super().__init__(token,username)

    def verify(self, ip=None):

        with db_session:
            try:
                now = datetime.datetime.now()
                valid_until = found_token.valid_until
                found_token = self.type.get(token=self.token)
                user = found_token.user
                if now <= valid_until:
                    user.activated = True
                    found_token.delete()
                    self.token = None
                    self.username = user.username
                    return True
                else:
                    return False
            # no token given or no token found
            except (ValueError, AttributeError):
                return False

    def create(self, valid_days=1):
        valid_until = datetime.datetime.now() + datetime.timedelta(days=valid_days)
        token_to_hash = f"{self.username}-activation;valid_until:{str(valid_until)}"
        print(token_to_hash)
        super().hash(token_to_hash)

        with db_session:
            try:
                found_user = self.config.db.User[self.username]
            except Exception:
                raise PyUserExceptions.MissingUserException

            token = self.config.db.ActivationCode.get(user=self.username)

            # create new token if no token exists
            if token is None:
                self.config.db.ActivationCode(user=found_user.username, token=self.token, valid_until=valid_until)

            # if token exists update it
            else:
                token.token = self.token
                token.valid_until = valid_until

            return True
