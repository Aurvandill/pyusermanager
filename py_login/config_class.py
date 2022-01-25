from pony.orm import *
from enum import Enum

from sqlalchemy import true

from db_config_class import DB_Config
from auth_type_enum import AuthTypeConverter


class LoginConfig():

    inited = False

    #some settings
    debug_output = False
    password_reset_days_valid = 1

    #for later understanding!
    auto_activate_accounts = True
    email_required = not auto_activate_accounts

    #lenghts
    username_min_len = 4
    password_min_len = 4

    db = Database()

    def __init__(self,db_config=DB_Config(),debug = False, password_reset_days_valid = 1, username_min_len = 4, password_min_len = 4, auto_activate_accounts = True):
        LoginConfig.debug_output = debug
        LoginConfig.username_min_len = username_min_len
        LoginConfig.password_min_len = password_min_len
        LoginConfig.auto_activate_accounts = auto_activate_accounts
        LoginConfig.email_required = not auto_activate_accounts
        LoginConfig.password_reset_days_valid = password_reset_days_valid

        if LoginConfig.debug_output:
            print(f"trying to bind with the following config{db_config}")

        if not LoginConfig.inited:

            LoginConfig.db.bind(provider = db_config.provider,
                            host = db_config.host,
                            port = db_config.port,
                            user = db_config.user,
                            passwd = db_config.pw,
                            db = db_config.db_name
                            )
            LoginConfig.db.provider.converter_classes.append((Enum,AuthTypeConverter))
                                  
            LoginConfig.db.generate_mapping(create_tables=True)

        LoginConfig.inited = True