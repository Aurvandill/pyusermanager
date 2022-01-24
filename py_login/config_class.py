from pony.orm import *
from enum import Enum

from db_config_class import DB_Config
from auth_type_enum import AuthTypeConverter


class LoginConfig():


    inited = False

    debug_output = False
    
    #lenghts
    username_min_len = 4
    password_min_len = 4

    db = Database()

    def __init__(self,db_config=DB_Config(),debug = False):
        LoginConfig.debug_output = debug

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