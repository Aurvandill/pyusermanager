from pony.orm import *
from . import custom_exceptions as ce


class Perm:
    def __init__(self, config, name):
        self.config = config
        self.perm_name = name

    def create(self):
        with db_session:
            # check if perm exists
            perm = self.config.db.Permissions.get(perm_name=self.perm_name)

            if perm is not None:
                return False
            else:
                # create perm
                perm = self.config.db.Permissions(perm_name=self.perm_name)

        return True

    def delete(self):
        with db_session:
            # check if perm exists
            perm = self.config.db.Permissions.get(perm_name=self.perm_name)

            if perm is None:
                return False
            else:
                # delete perm
                perm.delete()

        return True

    def assign_to_user(self, username=None):
        return self.perm_user(username, self.perm_name, True)

    def remove_from_user(self, username=None):
        return self.perm_user(username, self.perm_name, False)

    def get_all(self):
        perms = []

        with db_session:
            for perm in self.config.db.Permissions.select():
                perms.append(perm.perm_name)

        return perms

    def perm_user(self, username, perm, add):
        with db_session:
            user = self.config.db.User.get(username=username)
            if user is None:
                raise ce.MissingUserException("User to assign Perms to does not exist!")
            # check if user has perm
            found_perm = self.config.db.Permissions.get(perm_name=perm)
            if found_perm is not None:
                if add:
                    user.perms.add(found_perm)
                else:
                    user.perms.remove(found_perm)
                return True

        return False
