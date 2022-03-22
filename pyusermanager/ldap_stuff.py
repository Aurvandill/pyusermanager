import ldap


class LdapStuff:
    def __init__(self, config):
        self.config = config

    def authenticate(self, username, password):
        conn = ldap.initialize(self.config.address)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)

        # add ad suffix if it does not exist!
        if not username.endswith(self.config.suffix):
            username = f"{username}{self.config.suffix}"
        conn.simple_bind_s(username, password)
        return conn

    def get_ldap_groups(self, username:str, password:str) -> list:

        ldap_c = self.authenticate(username, password)
        userfilter = f"(&(objectClass=user)(sAMAccountName={username}))"
        userresults = ldap_c.search_s(
            self.config.base_dn, ldap.SCOPE_SUBTREE, userfilter, None
        )[0][1]["memberOf"]
        groups = []
        for group in userresults:
            group = group.decode("utf-8")
            group = group[group.index("CN=") + 3 : group.index(",")]
            groups.append(group)
        return groups

    def login(self, username:str, password:str) -> bool:
        try:
            groups = self.get_ldap_groups(username, password)
            if self.config.group in groups:
                return True
            else:
                return False
        except Exception as err:
            return False


# if __name__ == "__main__":
#    print(get_ldap_groups(sys.argv[1],sys.argv[2]))
