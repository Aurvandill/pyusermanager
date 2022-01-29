from pony.orm import *
from enum import Enum

from pyusermanager.Config import DB_Config
from pyusermanager.auth_type_enum import *

from pyusermanager.Config import AbstractConfig
from pyusermanager.Config import DB_Config
from pyusermanager.Config import AD_Config


class General_Config(AbstractConfig):

    # some settings
    debug_output = False
    password_reset_days_valid = 1

    # for later understanding!
    auto_activate_accounts = True
    email_required = not auto_activate_accounts

    # lenghts
    username_min_len = 4
    password_min_len = 4

    # do we allow public registrations?
    public_registration = True
    allow_avatars = True
    admin_group_name = "admin"

    dbcfg = DB_Config()
    adcfg = AD_Config()

    bound = False

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.db = Database()
        
    def bind(self):
        if not self.bound:
            self.db.bind(
                provider=self.dbcfg.provider,
                host=self.dbcfg.host,
                port=self.dbcfg.port,
                user=self.dbcfg.user,
                passwd=self.dbcfg.pw,
                db=self.dbcfg.db_name,
            )
            self.db.provider.converter_classes.append((Enum, AuthTypeConverter))
            #self.db.Entity.
            self.db.generate_mapping(create_tables=True,check_tables=True)

        self.bound = True
