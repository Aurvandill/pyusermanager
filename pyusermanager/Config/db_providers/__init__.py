from enum import Enum
from .prov_base import *
from .prov_mysql import *
from .prov_cockroachdb import *
from .prov_oracle import *
from .prov_postgresql import *
from .prov_sqlite import *


class DBProviders(Enum):

    mysql = MYSQL_Provider
    cockroachdb = CockroachDB_Provider
    oracle = Oracle_Provider
    postgresql = PostgreSQL_Provider
    sqlite = SQLite_Provider
    