from . import DB_Provider
from typing import Optional


class MYSQL_Provider(DB_Provider):
    provider: Optional[str] = "mysql"
    host: Optional[str] = "127.0.0.1"
    port: Optional[int] = 3306
    user: Optional[str] = "testuser"
    passwd: Optional[str] = "testpassword"
    db: Optional[str] = "user"
