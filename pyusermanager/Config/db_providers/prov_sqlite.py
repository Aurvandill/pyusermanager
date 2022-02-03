from . import DB_Provider
from typing import Optional


class SQLite_Provider(DB_Provider):
    provider: Optional[str] = "sqlite"
    filename: Optional[str] = "database.sqlite"
    create_db: Optional[bool] = True
