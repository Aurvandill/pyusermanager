

#LoginConfig(debug=True)


from pyusermanager import *


ad_config = AD_Config()
print(ad_config)

config = DB_Config(provider = "mysql", host = "127.0.0.1",port = 3306, user = "test", pw = "test123", db_name = "users")
ree = LoginConfig(config,True,1,4,4,False)

try:
    print(create_user(uname="admin",pw="12345",email="test@local",auth=AUTH_TYPE.LOCAL))
except Exception as err:
    print(err)

print(get_all_perms())

user_dict,token_dict,perms_dict = get_extended_info("admin")

print(login_user("admin","12345"))

try:
    print(login_user("testuser@ad.local","12345"))
except Exception as err:
    print(f"{type(err).__name__}: {err}")


token = create_token("admin",token_type=Auth_Token)

print(f"\ncreated token: {token}")

print("\ntrying to verify token")
success, perm_array, username = verify_token(token,"127.0.0.1")

print(success)
print(perm_array)
print(username)

print("\nchanging password and trying to verify token again!")
update_password("admin","newpw")

print("\ntrying to verify token")
success, perm_array, username = verify_token(token,"127.0.0.1")

print(success)
print(perm_array)
print(username)

print("\ninvalidating token")
try:
    print(logout_user(token))
except Exception as err:
    print(f"{type(err).__name__}: {err}")

try:
    print("\ntrying to verify token")
    success, perm_array, username = verify_token(token,"127.0.0.1")
    print(success)
    print(perm_array)
    print(username)
except Exception as err:
    print(f"{type(err).__name__}: {err}")




print("trying to invalidate already invalidated token")
print(logout_user(token))

print("trying to validate non existing token")
try:
    print(logout_user("doesnotexist"))
except Exception as err:
    print(f"{type(err).__name__}: {err}")

print("\ntrying to create reset and activation token!")
reset_token = create_token("admin",token_type=ResetCode)
activation_token = create_token("admin",token_type=ActivationCode)

print(f"reset_token: {reset_token}")
print(f"activation_token: {activation_token}")

print("\n---------------\nverifying other tokens!\n---------------")
print(f"Reset-Token: {verify_token(reset_token,token_type=ResetCode)}")
print(f"getting activation_token: {get_token('admin',ActivationCode)}")
print(f"activation-Token: {verify_token(activation_token,token_type=ActivationCode)}")
print(f"getting activation_token: {get_token('admin',ActivationCode)}")

print("\n---------------\ncreating groups and assigning admin to it!\n---------------")

print(f"create group reeee: {create_perm('reeee')}")
print(f"create group admin: {create_perm('admin')}")
print(f"assigning admin group admin: {assign_perm_to_user('admin','admin')}")
print(f"assigning admin group reeee: {assign_perm_to_user('admin','reeee')}")
print(f"remove admin from group reeee: {remove_perm_from_user('admin','reeee')}")
print(f"remove admin from group reeee(again): {remove_perm_from_user('admin','reeee')}")

print(f"getting Auth_Token: {get_token('admin',Auth_Token)}")
print(f"getting reset_Token: {get_token('admin',ResetCode)}")
print(f"getting activation_token: {get_token('admin',ActivationCode)}")

print(f"\ncurrent user (as dictionary): \n{get_users()}")
print()
try:
    print(create_user(uname="admin2",pw="12345",email="test@local",auth=AUTH_TYPE.LOCAL))
except Exception as err:
    print(err)
print(f"\ncurrent user (as dictionary): \n{get_users()}")

print("deleting test account!")
delete_user("admin")
delete_user("admin2")