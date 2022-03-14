from pony.orm import *
from pyusermanager import custom_exceptions as PyUserExceptions

class Perm:
    """A class to manage Permission/Usergroups"""

    def __init__(self, config, name = "not_given"):
        """Initing of the Object
        Parameters:
        config (General_Config): general configuration of the library
        name (str): name of the Group/Perm
        """
        self.config = config
        self.perm_name = name

    def create(self):
        """Creates the Permission/Group
        returns:
        succes (bool): was the opperation successfull?
        """
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
        """Deletes the Permission/Group
        returns:
        succes (bool): was the opperation successfull?
        """
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
        """Assigns a perm to a user
        Parameters:
        username (str): user to add the perm to

        returns:
        success (bool): was the opperation successfull?

        Exceptions:
        PyUserExceptions.MissingUserException -> If user was not found
        """
        return self.perm_user(username, True)

    def remove_from_user(self, username=None):
        """remove a perm from a user
        Parameters:
        username (str): user to remove the perm from

        returns:
        success (bool): was the opperation successfull?

        Exceptions:
        PyUserExceptions.MissingUserException -> If user was not found
        """
        return self.perm_user(username, False)

    def get_all(self):
        """This Function returns a list of all Perms in the DB"""
        perms = []

        with db_session:
            for perm in self.config.db.Permissions.select():
                perms.append(perm.perm_name)

        return perms

    def perm_user(self, username, add):
        """Assign or remove a perm from a User
        Parameters:
        username (str): user to remove the perm from
        add (bool): if true adds a perm if false removes the perm

        returns:
        success (bool): was the opperation successfull?

        Exceptions:
        PyUserExceptions.MissingUserException -> If user was not found
        """
        with db_session:
            user = self.config.db.User.get(username=username)
            if user is None:
                raise PyUserExceptions.MissingUserException("User to assign Perms to does not exist!")
            # check if user has perm
            found_perm = self.config.db.Permissions.get(perm_name=self.perm_name)
            if found_perm is not None:
                if add:
                    user.perms.add(found_perm)
                else:
                    user.perms.remove(found_perm)
                return True

        return False
