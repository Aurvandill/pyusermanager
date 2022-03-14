class NotInitedException(Exception):
    """Deprecated! was used to state that the database in the general config was not inited yet"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MissingUserException(Exception):
    """The requested User could not be found"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AlreadyExistsException(Exception):
    """The thing that was tried to create already existed"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class TokenMissingException(Exception):
    """No token was provided even though it was needed"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class NotAnADUser(Exception):
    """the user is not an AD user so you cant log him in via the AD Login handler"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class ADLoginProhibited(Exception):
    """Ad Logins are disabled so you cant log him in via the AD Login handler"""
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
