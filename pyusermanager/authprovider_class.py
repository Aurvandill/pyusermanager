from pony.orm import Database
from .Config import General_Config
from . import Token
from .user_funcs import user


class AuthProvider:

    def __init__(self,pyusermanagerconfig:General_Config)-> None:
        self.cfg = pyusermanagerconfig
        pass


    def is_logged_in(self,token:str,ip:str)-> tuple[bool,str]:

        try:
            auth_token = Token.Auth(self.cfg, token)
            success = auth_token.verify(ip)
            return success, auth_token.username
        except Exception as err:
            print(err)
            return False, ""

    def is_in_group(self,token:str,*,ip:str = None,groupname:str=None,groupnames:list[str]=None)->bool:

        returnvalue = False
        try:
            auth_token = Token.Auth(self.cfg, token)
            if ip is not None:
                success = auth_token.verify(ip)
                if success is False:
                    return False
            auth_token.get_user()
            user_dict = user(self.cfg, auth_token.username).info_extended()
            print(user_dict)
            if groupname in user_dict["perms"]:
                returnvalue = True

            for groups in groupnames:
                if groups in user_dict["perms"]:
                    returnvalue = True

        except Exception as err:
            print(err)
            pass

        return returnvalue

    async def is_in_group_by_name(self, username: str, *,group: str = None,groups:list[str]=None):
        """checks if a user is in the specified group"""

        try:
            found_user = user(self.cfg, username)
            userinfo = found_user.info_extended()
            if group in userinfo["perms"]:
                return True

            for group in groups:
                if group in userinfo["perms"]:
                    return True

        except Exception as err:
            pass

        return False

