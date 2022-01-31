from pyusermanager.Config.db_providers import DB_Provider
from typing import Optional


class PostgreSQL_Provider(DB_Provider):
    provider: Optional[str] = "postgres"
    user: Optional[str] = "testuser"
    password: Optional[str] = "testpassword"
    host: Optional[str] = "127.0.0.1"
    database: Optional[str] = "users"
