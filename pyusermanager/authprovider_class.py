from pony.orm import Database
from .Config import General_Config
from . import Token
from .user_funcs import user
from typing import Union

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

    def is_in_group(self,token:str,ip:str,groupnames: Union[str,list[str]])->bool:

        returnvalue = False
        try:
            auth_token = Token.Auth(self.cfg, token)
            success = auth_token.verify(ip)
            if success is False:
                return False
            auth_token.get_user()
            user_dict = user(self.cfg, auth_token.username).info_extended()
        except Exception as err:
            print(err)
            pass

        if type(groupnames) is str:
            groupnames = [groupnames]

        return any(item in groupnames for item in user_dict["perms"])

    async def is_in_group_by_name(self, username: str,groups:Union[str,list[str]]=None):
        """checks if a user is in the specified group"""

        try:
            found_user = user(self.cfg, username)
            userinfo = found_user.info_extended()
            
        except Exception as err:
            return False

        if type(groupnames) is str:
            groupnames = [groupnames]

        return any(item in groupnames for item in userinfo["perms"])

