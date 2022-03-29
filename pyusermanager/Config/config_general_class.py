from pony.orm import *
from enum import Enum

from pyusermanager import DefineEntitys, AuthTypeConverter

from . import AbstractConfig
from . import AD_Config

class General_Config(AbstractConfig):
    """a Configuration class storing our General config"""

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

    adcfg = AD_Config()

    bound = False
    avatar_folder = "./avatars"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Database()

    def bind(self, db_provider):
        if not self.bound:
            self.db.bind(db_provider.__dict__)

            self.db.provider.converter_classes.append((Enum, AuthTypeConverter))

            DefineEntitys(self.db)

            self.db.generate_mapping(create_tables=True, check_tables=True)

        self.bound = True
