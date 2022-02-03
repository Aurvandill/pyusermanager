from abc import ABC
from dataclasses import dataclass


@dataclass
class DB_Provider(ABC):
    def __init__(self, *args, **kwargs):

        if args:
            raise ValueError("please init with keyword arguments")
        # check if arg exists in class

        if "provider" in kwargs:
            raise ValueError("cant change provider string!")

        # set all default values from class
        for key, val in self.__class__.__dict__["__annotations__"].items():
            self.__setattr__(key, self.__getattribute__(key))

        for key, val in kwargs.items():
            # check if key is in var
            # if not will rais exception!
            self.__getattribute__(key)
            # set it
            self.__setattr__(key, val)

    def __str__(self):
        work_dict = {**type(self).__dict__, **self.__dict__}
        returnstring = f"\n--------{self.__class__.__name__}--------\n"
        # print(work_dict)
        for key, val in work_dict.items():
            if not key.startswith("_"):
                reee = f"{''.ljust(10-len(key),' ')}{key}: {val}\n"
                returnstring += reee

        return returnstring
