from pony.orm import db_session
from pyusermanager import PyUserExceptions
from pyusermanager.Token import Token


###########################
#
# Activation Token
#
###########################
class Activation(Token):
    def __init__(self, config, token=None, username=None):
        self.config = config
        self.type = self.config.db.ActivationCode
        super().__init__(token)

    def verify(self, ip=None):
        with db_session:
            try:
                found_token = self.type.get(token=self.token)
                user = found_token.user
                user.activated = True
                found_token.delete()
                self.token = None
                self.username = user.username
                return True
            # no token given or no token found
            except (ValueError, AttributeError):
                return False

    def create(self):
        token_to_hash = f"{self.username}-activation"
        self.hash(token_to_hash)

        with db_session:
            try:
                found_user = self.config.db.User[self.username]
            except Exception:
                raise PyUserExceptions.MissingUserException

            token = self.config.db.ActivationCode.get(user=self.username)

            # create new token if no token exists
            if token is None:
                self.config.db.ActivationCode(
                    user=found_user.username, token=self.token
                )

            # if token exists update it
            else:
                token.token = self.token

            return True
