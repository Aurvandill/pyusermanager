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

print(login_user("admin","12345"))



try:
    print(login_user("testuser@ad.local","12345"))
except Exception as err:
    print(f"{type(err).__name__}: {err}")


token = create_token("admin")

print(f"\ncreated token: {token}")

print("\ntrying to verify token")
success, perm_array, username = verify_token(token,"127.0.0.1")

print(success)
print(perm_array)
print(username)

print("\ninvalidating token")

print(logout_user(token))


print("\ntrying to verify token")
success, perm_array, username = verify_token(token,"127.0.0.1")

print(success)
print(perm_array)
print(username)


print("trying to invalidate already invalidated token")
print(logout_user(token))

print("trying to validate non existing token")
try:
    print(logout_user("doesnotexist"))
except Exception as err:
    print(f"{type(err).__name__}: {err}")
