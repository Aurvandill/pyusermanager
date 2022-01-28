from pony.orm import *
from . import data_classes as dc
from . import custom_exceptions as ce


class Perm:
    def create(perm_name=None):
        with db_session:
            # check if perm exists
            perm = dc.Permissions.get(perm_name=perm_name)

            if perm is not None:
                return False
            else:
                # create perm
                perm = dc.Permissions(perm_name=perm_name)

        return True

    def delete(perm_name=None):
        with db_session:
            # check if perm exists
            perm = dc.Permissions.get(perm_name=perm_name)

            if perm is None:
                return False
            else:
                # delete perm
                perm.delete()

        return True

    def assign_to_user(username=None, perm=None):

        with db_session:
            user = dc.User.get(username=username)
            if user is None:
                raise ce.MissingUserException("User to assign Perms to does not exist!")
            else:
                found_perm = dc.Permissions.get(perm_name=perm)
                if found_perm is not None:
                    user.perms.add(found_perm)
                    return True

        return False

    def remove_from_user(username=None, perm=None):
        with db_session:
            user = dc.User.get(username=username)
            if user is None:
                raise ce.MissingUserException("User to assign Perms to does not exist!")
            else:
                # check if user has perm
                found_perm = dc.Permissions.get(perm_name=perm)
                if found_perm is not None:
                    user.perms.remove(found_perm)
                    return True

        return False

    def get_all():
        perms = []

        with db_session:
            for perm in dc.Permissions.select():
                perms.append(perm.perm_name)

        return perms
