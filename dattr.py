import json
import typing
import keyword
import os
from collections import abc
import sys

# from dattr_helper import DictAttrDict

class DictAttr(object):
    """
        Interpretation of dictionary keys as Attributtes using dot(.) notation.
        The class is designed to be a semi-singleton class to handle recurrsive path update.
    """
    # _DICT_ATTR_OBJ: DictAttr
    # def __new__(cls, *args, *kwargs):
    #     """
    #         If object already available and `singleton` argument is provided as False, return the same.
    #         Else create new object.
    #     """
    #     if cls.__name__ == 'DictAttr':
    #         if _DICT_ATTR_OBJ and kwargs.get('singleton', False):
    #             return _DICT_ATTR_OBJ
    #         else:
    #             return super(DictAttr, cls).__new__(cls)
    #     else:
    #         return super(DictAttr, cls).__new__(cls)

    def __init__(self, data:typing.Union[typing.Dict, typing.List, str, int]):
        """
            Initializing Object.
        """
        self._data = data
        self._path = []

    """Alternate constructors"""
    @classmethod
    def from_string(cls, value:str):
        """
            Alternate constructor to build from string representation.
            param: value:str
        """
        return cls(json.loads(value))

    @classmethod
    def from_json_file(cls, filepath):
        """
            Alternate constructor to build from string representation.
            param: value:str
        """
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                json_data = json.load(f)
            return cls(json_data)
        else:
            # TODO: Raise File does not exists exception.
            raise Exception('File does not exists!')

    """Helper function"""
    def _get_current_data(self):
        data = self._data
        for elem in self._path:
            data = data[elem]
        return data

    """Meta-programming"""
    def __getitem__(self, key):
        if isinstance(key, slice) or isinstance(key, str) or isinstance(key, int):
            current_data = self._get_current_data()
            if isinstance(current_data, abc.Mapping):
                val = current_data.get(key, None)
            else:
                val = current_data[key]
            if val:
                return DictAttrSub(self._data, self._path + [key])
            else:
                # TODO: Raise Invalid Key execption
                raise Exception('KeyError')
        else:
            # TODO: Raise Invalid type argument
            raise Exception('Invalid argument type: {}'.format(type(key)))

    def __getattr__(self, key:str):
        """
            Check if accessed key is an identifier of Python dictionary. Else return the DictAttr object for the corrsponding value of the key.
        """
        current_data = self._get_current_data()
        if hasattr(current_data, key):
            return getattr(current_data, key)
        else:
            val = current_data.get(key, None)
            if val:
                return DictAttrSub(self._data, self._path + [key])
            else:
                # TODO: Raise Invalid Key execption
                raise Exception('KeyError')

    """Callable(If required)"""
    def __call__(self, *args, **kwargs):
        pass
    
    """Output handling"""
    def __str__(self):
        # if isinstance(self._get_current_data(), abc.Mapping):
        #     return f"DictAttr<{[key for key in self._data.keys()]}>"
        # elif isinstance(self._get_current_data(), abc.MutableSequence):
        #     elem = "DictAttr<(...)>"
        #     return f"DictAttr<{[elem for _ in self._data]}>"
        # else:
        #     return str(self._get_current_data())
        return str(self._get_current_data())
    
    def __repr__(self):
        return 'DictAttr(' + str(self._get_current_data()) + ')'

    # def to_dict(self) -> typing.Dict:
    #     return self._data

    def to_string(self) -> str:
        return json.dumps(self._data)
    
    def to_json_file(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump(self._data, f)
        else:
            # TODO: Raise File does not exists exception.
            raise Exception('File does not exists!')

    # def __setitem__(self, _index, _value):
    #     if _index >= len(self.__value):
    #         # TODO: Raise Index out of bound exception.
    #         raise Exception("List assignment Index out of bound execption!")
    #     self.__value[_index] = _value

    # def to_list(self) -> typing.List:
    #     return self.__value


class DictAttrSub(DictAttr):
    def __init__(self, data:typing.Union[typing.Dict, typing.List, str, int], path:list):
        super().__init__(data)
        self._path = path


if __name__ == "__main__":
    dattr_obj = DictAttr({
        "Dummy_Key": "Dummy_Data",
        "Dummy_List": [
            {
                "Dummy_Mapping": {
                    "keys": "Dummy_Value_In_Mapping"
                }, 
                "Dummy_Flag":1
            }
        ]})
    # return DictAttr.from_string('{"Dummy_Key": "Dummy_Data","Dummy_List": [{"Dummy_Mapping": {"keys": "Dummy_Value_In_Mapping"},"Dummy_Flag":100}]}')
    print(dattr_obj.to_string())
    print(dattr_obj.Dummy_List)
    print(dattr_obj.Dummy_List[0].Dummy_Mapping)
    print(dattr_obj.Dummy_List[0].Dummy_Mapping['keys'])
    print(dattr_obj.Dummy_List[0].Dummy_Mapping.keys())
    # dattr_obj.Dummy_List[0] = 'Dummy_Replaced_Value'
    # print(dattr_obj.Dummy_List[0])
    # print(dattr_obj.to_string())
    # print(dattr_obj.Dummy_Mapping.keys())