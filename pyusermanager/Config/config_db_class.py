from pyusermanager.Config import AbstractConfig


class DB_Config(AbstractConfig):
    provider="mysql",
    host="127.0.0.1",
    port=3306,
    user="testuser",
    pw="testpassword",
    db_name="user",
