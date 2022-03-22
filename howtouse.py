from pyusermanager import *
from pyusermanager.Config import *
from pyusermanager.Config.db_providers import *
import pyusermanager.Token as Token


print("setting up database Connector")
# Create DB-Config
db_cfg = MYSQL_Provider(
    host="127.0.0.1", port=3306, user="test", passwd="test1234", db="users"
)

print("setting up general Config")
# setup general config
cfg = General_Config(auto_activate_accounts=False)

print("binding to database")
# connect to db
cfg.bind(db_cfg)

print("Creating testuser")
#creating user
try:
    user(cfg, "testuser").create("password")
except PyUserExceptions.AlreadyExistsException:
    print("user already exists")

print("\n-----------------------")
print("Login Function examples")
print("-----------------------\n")
#Trying to Login with correct credentials
try:
    print(f"Login success: {login(cfg,'testuser','password')}")
except PyUserExceptions.MissingUserException:
    print("user not found")

#Trying to Login with wrong credentials
try:
    print(f"Login success: {login(cfg,'testuser','password123')}")
except PyUserExceptions.MissingUserException:
    print("user not found")

#Trying to Login not existing User
try:
    print(f"Login success: {login(cfg,'doesnotexist','password')}")
except PyUserExceptions.MissingUserException:
    print("user not found")

print("\n--------------")
print("Token Examples")
print("--------------\n")

#if login was successfull we want to create an auth token and print it
if login(cfg,'testuser','password'):
    token = Token.Auth(cfg,username="testuser")
    token.create("127.0.0.1",valid_days=1)
    print(f"Token: {token.token}")


#try to create Token for an not existing user
try:
    invalidtoken = Token.Auth(cfg,username="doesnotexist")
    invalidtoken.create("127.0.0.1",valid_days=1)
    print(f"Token: {invalidtoken.token}")
except PyUserExceptions.MissingUserException:
    print("user to create Token for does not exist")


#now to verifying tokens!

print("\n---------------")
print("veryfing tokens")
print("---------------\n")

print("creating testtoken object")
testtoken = Token.Auth(cfg,token=token.token)
print(f"trying to verify Token: {testtoken.token}\nreturnes: {testtoken.verify('127.0.0.1')}")
print(f"trying to verify Token from another ip: {testtoken.token}\nreturnes: {testtoken.verify('192.168.0.1')}")

print("setting token lifetime to 10 days")
testtoken.set_lifetime(10)

print("creating testtoken2 object")
testtoken2 = Token.Auth(cfg,token="this token does not exist!")
print(f"trying to verify Token: {testtoken2.token}\nreturnes: {testtoken2.verify('127.0.0.1')}")

print (f"testtoken:{testtoken}")
print (f"testtoken2:{testtoken2}")

print("as we see a successfull token verification gives us an username!")
print("but be carefull if you use the same object to verify another token or anything else the username does not get updated!")
print("(this behaviour might get changed in the future)")


print("\n----------------------------------")
print("Creating and assigning Permissions")
print("----------------------------------\n")

testperm = Perm(cfg,"testperm")
print(f"tyring to create perm testperm: {testperm.create()}")
print(f"tyring to assign it to testuser: {testperm.assign_to_user('testuser')}")
try:
    print(f"trying to assign it to a not existing user: {testperm.assign_to_user('does not exist')}")
except PyUserExceptions.MissingUserException:
    print("user was not found so we cant assign an perm")

#now we try to assing a perm which does not exist in the db!
testperm2 = Perm(cfg,"this perm does not exist")

print(f"trying to assign a not existing perm to testuser: {testperm2.assign_to_user('testuser')}")
print("Note this does not throw an exception it just returns False. This behaviour might change in the future")



print("\n-----------------------------------------------------")
print("Activation Code generation and Error Token generation")
print("-------------------------------------------------------\n")

reset = Token.Reset(cfg,username="testuser")
reset.create(1)
reset.set_lifetime(10)

act = Token.Activation(cfg,username="testuser")
act.create(1)
act.set_lifetime(10)