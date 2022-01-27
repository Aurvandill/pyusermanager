Introduction
==================
Hello and Welcome to the Documentation of pyusermanager

This Project is aimed to simplify building apis which require User
authentification


1. Features
-------------

-  login
-  registration
-  Token generation
-  Token Verification
-  Different Token Types

   -  Auth_Token -> Used for user verification
   -  ResetCode -> Used to auth password Resets
   -  ActivationCode -> Used to activate user Accounts

-  Custom Exceptions

   -  MissingUserExceptions
   -  NotInitedException
   -  AlreadyExistsException
   -  TokenMissingException

2. Plans for the Future
-------------------------

-  ☐ Write Docs

   -  ☑ Created readthedocs page

-  ☐ Refactor db_functions.py (v.2.x.x)
-  ☐ Custom Return Object instead of dicts
-  ☐ fix Code Smells
-  ☑ implement token verification for other tokens than auth_token
-  ☐ implement propper logging

3. Changelog
---------------

v1.0.5 (`git <https://github.com/Aurvandill137/pyusermanager/releases/tag/v1.0.5>`__) (`pypi <https://pypi.org/project/pyusermanager/1.0.5/>`__)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changed
~~~~~~~~
-  get_extended_info not takes an extra optional arg (include_email) if
   its not None it will return the user email in the user_dict

Added
~~~~~~
-  docs folder
  
Changed
~~~~~~~~

-  README.md