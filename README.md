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

# Dev Branch
experimentation and other stuff

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
- [5. Changelog](#5-changelog)

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
- [ ] uth_type_enum
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

# 5. Changelog

## v1.0.5 ([git](https://github.com/Aurvandill137/pyusermanager/releases/tag/v1.0.5)) ([pypi](https://pypi.org/project/pyusermanager/1.0.5/))
### Changed
* get_extended_info not takes an extra optional arg (include_email) if its not None it will return the user email in the user_dict
