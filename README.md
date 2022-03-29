<h1 align="center">pyusermanager</h1>
<h3 align="center">a user management libary for web services or other stuff</h3>
<br>
<p align="center">
<a href="https://pypi.org/project/pyusermanager/"><img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/pyusermanager"></a>
<a href="https://pypi.org/project/pyusermanager/"><img height="20" alt="Supported python versions" src="https://img.shields.io/pypi/pyversions/pyusermanager"></a>
<br>
<a href="https://pypi.org/project/black"><img height="20" alt="Black badge" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://codeclimate.com/github/Aurvandill137/pyusermanager/maintainability"><img src="https://api.codeclimate.com/v1/badges/97cf369553f228ce3a3c/maintainability" /></a>
<br>
<a href="https://codeclimate.com/github/Aurvandill137/pyusermanager/test_coverage"><img src="https://api.codeclimate.com/v1/badges/97cf369553f228ce3a3c/test_coverage" /></a>
<a href="https://pyusermanager.readthedocs.io/en/latest/"><img height="20" alt="Documentation status" src="https://img.shields.io/badge/documentation-up-00FF00.svg"></a>
</p>

# 1. Info

This Project is aimed to simplify building apis which require User authentification

## 1.2 Table of Contents

- [1. Info](#1-info)
  - [1.2 Table of Contents](#12-table-of-contents)
- [2. Features](#2-features)
- [3. Plans for the Future](#3-plans-for-the-future)
- [4. Documentation Status](#4-documentation-status)
  - [4.1 General](#41-general)
  - [4.2 Modules](#42-modules)
- [5. Quickstart](#5-quickstart)
- [6. Changelog](#6-changelog)

# 2. Features

* login
* registration
* Token generation
* Token Verification
* Different Token Types
  * Auth_Token      -> Used for user verification
  * ResetCode       -> Used to auth password Resets
  * ActivationCode  -> Used to activate user Accounts
* Custom Exceptions
  * MissingUserExceptions
  * NotInitedException
  * AlreadyExistsException
  * TokenMissingException

# 3. Plans for the Future

- [x] ~~Refactor db_functions.py (v.2.0.0)~~
- [ ] Custom Return Object instead of dicts
- [x] ~~fix Code Smells~~
- [x] ~~implement token verification for other tokens than auth_token~~
- [ ] implement propper logging (v.2.1.0)
- [ ] writing Tests
    - [ ] Token Module
    - [ ] Config Module
    - [ ] Perm Module
    - [ ] UserFunctions
    - [ ] Login Functions

# 4. Documentation Status

## 4.1 General

- [x] ~~Created readthedocs page~~
- [ ] How to Install
- [ ] How to Use


## 4.2 Modules

- [ ] auth_type_enum
- [ ] custom_exceptions
- [ ] data_classes
- [ ] ldap_stuff
- [ ] login_class
- [ ] perms_class
- [ ] user_funcs
- [ ] Token
     - [ ] token_base_class
     - [ ] token_auth_class
     - [ ] token_reset_class
     - [ ] token_activation_class
- [ ] Config</li>
     - [ ] config_base_class
     - [ ] config_ad_class
     - [ ] config_db_class
     - [ ] config_general_class

# 5. Quickstart

```python

from pyusermanager import *
from pyusermanager.Config import *
from pyusermanager.Config.db_providers import *
import pyusermanager.Token as Token

# Create DB-Config
db_cfg = MYSQL_Provider(
    host="127.0.0.1", port=3306, user="test", passwd="test1234", db="users"
)
# setup general config
cfg = General_Config(auto_activate_accounts=False)
# connect to db
cfg.bind(db_cfg)

#creating user
try:
    user(cfg, "testuser").create("password")
except PyUserExceptions.AlreadyExistsException:
    print("user already exists")

#if login was successfull we want to create an auth token and print it
if login(cfg,'testuser','password'):
    token = Token.Auth(cfg,username="testuser")
    token.create("127.0.0.1",valid_days=1)
    print(f"Token: {token.token}")

testtoken = Token.Auth(cfg,token=token.token)
print(f"trying to verify Token: {testtoken.token}\nreturnes: {testtoken.verify('127.0.0.1')}")

#creating a perm and assigning it to a user
testperm = Perm(cfg,"testperm")
testperm.create()
print(f"tyring to assign it to testuser: {testperm.assign_to_user('testuser')}")


```

more examples can be found in howtouse.py


# 6. Changelog

## v2.0.6 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v2.0.6)) ([pypi](https://pypi.org/project/pyusermanager/2.0.6/))

### Changed

* avatar folder is now part of the general config

## v2.0.5 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v2.0.5)) ([pypi](https://pypi.org/project/pyusermanager/2.0.5/))

### Changed

* added DBProviders enum to pyusermanager.Config.db_providers so we can get the fitting db provider by the specified name
* fixed some typos in the readme
* fixed some typos in howtouse.py

## v2.0.4 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v2.0.4)) ([pypi](https://pypi.org/project/pyusermanager/2.0.4/))

### Changed

* an ad user will now get ad groups on every login (will remove groups set by hand!)
* new exception ADLoginProhibited which will be raised if an already existing ad user tries to login after ad logins where disabled

## v2.0.3 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v2.0.3)) ([pypi](https://pypi.org/project/pyusermanager/2.0.3/))

### Changed

* fixed bug in activation token creation
* you can now set the lifetime of a token with set_lifetime on the token object

## v2.0.2 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v2.0.2)) ([pypi](https://pypi.org/project/pyusermanager/2.0.2/))

### Changed

* auth_token now updates last_login attribute in database

## v2.0.1 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v2.0.1)) ([pypi](https://pypi.org/project/pyusermanager/2.0.1/))

### Changed

* alot of rewrites
* please look at the howtouse.py and documentation!

## v1.0.5 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v1.0.5)) ([pypi](https://pypi.org/project/pyusermanager/1.0.5/))

### Changed

* get_extended_info not takes an extra optional arg (include_email) if its not None it will return the user email in the user_dict
