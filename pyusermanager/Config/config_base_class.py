

from abc import ABC, abstractmethod


class AbstractConfig(ABC):
    def __init__(self,*args,**kwargs):
        
        obj = self.__class__
        if args:
            raise ValueError("please init with keyword arguments")
        #check if arg exists in class

        for key, val in kwargs.items():
            #check if key is in var
            self.__getattribute__(key)
            #set it
            self.__setattr__(key,val)

    def __str__(self):
        work_dict = {**type(self).__dict__,**self.__dict__}
        returnstring = f"\n--------{self.__class__.__name__}--------\n"
        #print(work_dict)
        for key,val in work_dict.items():
            if not key.startswith("_"):
                reee = f"{''.ljust(10-len(key),' ')}{key}: {val}\n"
                returnstring += reee
            
        return returnstring
                
