from . import DB_Provider
from typing import Optional


class Oracle_Provider(DB_Provider):
    provider: Optional[str] = "oracle"
    user: Optional[str] = "testuser"
    password: Optional[str] = "testpassword"
    dsn: Optional[str] = None
