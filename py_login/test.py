from config_class import LoginConfig
from db_config_class import DB_Config
from ad_config_class import AD_Config
from custom_exceptions import *

from db_functions import *
from auth_type_enum import AUTH_TYPE
import data_classes


ad_config = AD_Config()
print(ad_config)

config = DB_Config(provider = "mysql", host = "127.0.0.1",port = 3306, user = "test", pw = "test123", db_name = "users")
ree = LoginConfig(config,True)

try:
    print(create_user("admin","12345",AUTH_TYPE.LOCAL))
except Exception as err:
    print(err)

print(get_all_perms())

user_dict,token_dict,perms_dict = get_extended_info("admin")
print(user_dict["auth_type"])
print(isinstance(user_dict["auth_type"],AUTH_TYPE))

print(login_user("admin","12345"))

print(login_user("testuser@ad.local","12345"))

