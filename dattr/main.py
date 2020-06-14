import json
import typing
import os
from collections import abc
import sys
import errno

# from dattr_helper import DictAttrDict

class DictAttr(object):
    """
        Interpretation of dictionary keys as Attributtes using dot(.) notation(with minor restrictions).
    """

    def __init__(self, data:typing.Union[typing.Dict, typing.List, str, int]):
        """
            Initializing Object. We will use setattr from object class, as setattr is overriden in DictAttrSub class.
            param: data
        """
        super().__setattr__('_data', data)
        super().__setattr__('_path', [])

    # Alternate constructors
    @classmethod
    def from_string(cls, value:str):
        """
            Alternate constructor to build from string representation.
            param: value
        """
        return cls(json.loads(value))

    @classmethod
    def from_json_file(cls, filepath):
        """
            Alternate constructor to build from string representation.
            param: filepath
        """
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                json_data = json.load(f)
            return cls(json_data)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filepath)

    def _get_current_data(self):
        """
            Helper function: Extracts value of current state.
        """
        data = self._data
        for elem in self._path:
            data = data[elem]
        return data

    # Meta-programming starts
    def __getitem__(self, key):
        """
            Handling data extraction via interpolation.
            param: key
        """
        if isinstance(key, slice) or isinstance(key, str) or isinstance(key, int):
            current_data = self._get_current_data()
            if isinstance(current_data, abc.Mapping):
                val = current_data.get(key, None)
            else:
                val = current_data[key]
            if val:
                return DictAttrSub(self._data, self._path + [key])
            else:
                if isinstance(key, slice) or isinstance(key, int):
                    raise IndexError(key)
                else:
                    raise KeyError(key)
        else:
            raise TypeError('Argument - {} is of invalid type: {}'.format(key, type(key)))

    def __getattr__(self, key:str):
        """
            Handling data extraction via (.) notation.
            Check if accessed key is an identifier of Python dictionary. Else return the DictAttr object for the corrsponding value of the key.
            param: key
        """
        current_data = self._get_current_data()
        if hasattr(current_data, key):
            return getattr(current_data, key)
        else:
            val = current_data.get(key, None)
            if val:
                return DictAttrSub(self._data, self._path + [key])
            else:
                raise KeyError(key)

    def __call__(self, *args, **kwargs):
        """
            Make the object Callable(Implement if required)
        """
        pass

    def __str__(self):
        """
            Setting the output of `str()` and `print()` function.
        """
        return str(self._get_current_data())

    def __repr__(self):
        """
            Setting represtation of the object.
        """
        return "DictAttr('" + str(self._get_current_data()) + "')"

    def __eq__(self, other):
        """
            Handling Equality, this will come into effect is the object is compared with any data.
            param: other
        """
        return str(self) == str(other)

    def __lt__(self, other):
        """
            Handling `less than` comparison, this will come into effect is the object is compared with any data.
            param: other
        """
        return str(self) < str(other)

    def __gt__(self, other):
        """
            Handling `greater than` comparison, this will come into effect is the object is compared with any data.
            param: other
        """
        return str(self) > str(other)

    def __le__(self, other):
        """
            Handling `greater than` comparison, this will come into effect is the object is compared with any data.
            param: other
        """
        return str(self) <= str(other)

    def __ge__(self, other):
        """
            Handling `greater than equals to` comparison, this will come into effect is the object is compared with any data.
            param: other
        """
        return str(self) >= str(other)

    # Alternate data access API
    def to_json_file(self, filepath):
        """
            Data will be stored in file in json format.
            param: filepath
        """
        with open(filepath, 'w') as f:
            json.dump(self._data, f)


class DictAttrSub(DictAttr):
    """
        Keeping the path of each level separate using separate objects.
    """

    def __init__(self, data:typing.Union[typing.Dict, typing.List, str, int], path:list):
        """
            Initializing Sub Object. This object will hold the path for current state.
            param: data
            param: path
        """
        super().__init__(data)
        super().__setattr__('_path', path)

    #Meta-programming starts
    def __setattr__(self, key:str, value):
        """
            Supporting data assignment using (.) notation - with minor caviates.
            param: key
            param: value
        """
        elem = self._get_current_data()
        elem[key] = value

    def __setitem__(self, key:str, value):
        """
            Supporting data assignment via interpolation.
            param: key
            param: value
        """
        self.__setattr__(key, value)


"""
    Dummy example set, if main.py is executed directly.
"""
if __name__ == "__main__":
    dattr_obj = DictAttr({
        "Dummy_Key": "Dummy_Data",
        "Dummy_List": [
            {
                "Dummy_Mapping": {
                    "keys": "Dummy_Value_In_Mapping"
                }, 
                "Dummy_Flag":2
            }
        ]})
    print(dattr_obj.Dummy_List)
    print(dattr_obj.Dummy_List[0].Dummy_Mapping)
    print(dattr_obj.Dummy_List[0].Dummy_Mapping['keys'])
    print(dattr_obj.Dummy_List[0].Dummy_Mapping.keys())
    dattr_obj.Dummy_List[0].Dummy_Mapping['keys'] = 'Dummy_Replaced_Value'
    print(dattr_obj.Dummy_List[0].Dummy_Mapping['keys'])
    dattr_obj.Dummy_List[0].Dummy_Mapping.keys = 'Dummy_Replaced_Again_Value'
    print(dattr_obj.Dummy_List[0].Dummy_Mapping['keys'])
    print(dattr_obj.Dummy_List[0].Dummy_Mapping.keys())
    for elem in dattr_obj.keys():
        print(dattr_obj[elem])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(dattr_obj.Dummy_List[0].Dummy_Flag == 2)
    print(dattr_obj.Dummy_List[0].Dummy_Flag < 3)
    print(dattr_obj.Dummy_List[0].Dummy_Flag <= 3)
    print(dattr_obj.Dummy_List[0].Dummy_Flag <= 2)
    print(dattr_obj.Dummy_List[0].Dummy_Flag >= 2)
    print(dattr_obj.Dummy_List[0].Dummy_Flag >= 1)
    print(dattr_obj.Dummy_List[0].Dummy_Flag > 1)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
