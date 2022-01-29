from pyusermanager.Config import AbstractConfig


class AD_Config(AbstractConfig):

    login = False
    address = "ldap://127.0.0.1:389"
    base_dn = "ou=User,dc=ad,dc=local"
    group = "allowed_to_login"
    suffix = "@ad.local"
