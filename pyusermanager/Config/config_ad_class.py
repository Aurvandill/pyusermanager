from .config_base_class import AbstractConfig


class AD_Config(AbstractConfig):
    """a Configuration class storing our AD Related config"""
    login = False
    address = "ldap://127.0.0.1:389"
    base_dn = "ou=User,dc=ad,dc=local"
    group = "allowed_to_login"
    suffix = "@ad.local"
