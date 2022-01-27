ad_config_class.py
===================
in This File the Class AD_Config is defined 


class AD_Config:
-------------------
This class contains Config Parameters for AD-Connections


vars
^^^^^^^^
- inited(bool)
   - default = False
   - was the config inited?
- ad_login(bool)
   - default = False
   - do we allow logins over the ad?
- ad_address(str)
   - default = "ldap://127.0.0.1:389"
   - base address of the ldap server we want to connect to
- base_dn(str)
   - default = "ou=User,dc=ad,dc=local"
   - base dn of Users
- ad_group(str)
   - default = "allowed_to_login"
   - a group required by the user to be allowed to log in.
- ad_suffix(str)
   - default = "@ad.local"
   - standard suffix for every user account

__init__
^^^^^^^^^^^^^^

inits the AD_Config object with passed vars

.. code-block:: python

    def __init__(self,ad_login = False, ad_address = "ldap://127.0.0.1:389", base_dn = "ou=User,dc=ad,dc=local", ad_group = "allowed_to_login", ad_suffix ="@ad.local"):
        if not AD_Config.inited:
            AD_Config.login = ad_login
            AD_Config.address = ad_address
            AD_Config.base_dn = base_dn
            AD_Config.group = ad_group
            AD_Config.suffix = ad_suffix

        AD_Config.inited = True


__str__
^^^^^^^^^^^^^^

returns the AD_Config Object as String

.. code-block:: python

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

