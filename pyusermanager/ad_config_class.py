class AD_Config:

    login = False
    address = "ldap://127.0.0.1:389"
    base_dn = "ou=User,dc=ad,dc=local"
    group = "allowed_to_login"
    suffix = "@ad.local"

    def __init__(self,ad_login=False):
        self.login = ad_login

    def __str__(self):
        return f"""
===============AD-Config===============

    ad_login:   {self.login}
    ad_address: {self.address}
    base_dn:    {self.base_dn}
    ad_group:   {self.group}
    ad_suffix:  {self.suffix}

=======================================
        """
