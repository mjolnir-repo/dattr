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
    """
    def __new__(cls, _obj:typing.Union[typing.Dict, typing.List, str]):
        """
            1. If received object is Mapping, return new object of the class,
            2. If it is a list, return list of objects,
            3. Else, return object.
        """
        if cls.__name__ == 'DictAttr':
            if isinstance(_obj, abc.Mapping):
                return DictAttrDict(_obj)
            elif isinstance(_obj, abc.MutableSequence):
                return DictAttrList(_obj)
            else:
                return _obj
        else:
            return super(DictAttr, cls).__new__(cls)

    @classmethod
    def from_string(cls, _value:str):
        """
            Alternate constructor to build from string representation.
            param: value:str
        """
        return cls(json.loads(_value))

    @classmethod
    def from_json_file(cls, _filepath):
        """
            Alternate constructor to build from string representation.
            param: value:str
        """
        if os.path.exists(_filepath):
            with open(_filepath, 'r') as _f:
                __json_data = json.load(_f)
            return cls(__json_data)
        else:
            # TODO: Raise File does not exists exception.
            raise Exception('File does not exists!')


class DictAttrDict(DictAttr):
    """
        When the object is mapping
    """
    def __init__(self, _dict_obj:typing.Dict):
        """
            Initializing Object.
        """
        self.__value = {}
        for _key, _value in _dict_obj.items():
            __key = self.__key_check(_key)
            self.__value[__key] = _value

    def __key_check(self, _key:str):
        """
            Checks:
                1. If provided key is a built-in dictionary attribute, raise exception.
                2. If provided key is a keyword, append '_' to the end.
                3. if provided key is not suited to be an identifier, raise exception
        """
        if _key in dir(dict()):
            # TODO: Raise Unsupported Identifier execption
            raise Exception('Unsupported Identifier execption!')
        elif keyword.iskeyword(_key) or _key in dir(self):
            return _key + '_'
        elif not _key.isidentifier():
            # TODO: Raise Invalid Identifier execption
            raise Exception('Invalid Identifier execption!')
        else:
            return _key

    def __getattr__(self, _key:str):
        """
            Check if accessed key is an identifier of Python dictionary. Else return the DictAttr object for the corrsponding value of the key.
        """
        if hasattr(self.__value, _key):
            return getattr(self.__value, _key)
        else:
            __key = self.__key_check(_key)
            __val = self.__value.get(__key, None)
            if __val:
                return DictAttr(__val)
            else:
                # TODO: Raise Invalid Key execption
                raise Exception('KeyError')

    # def __setitem__(self, _key, _value):
    #     __key = self.__key_check(_key)
    #     self.__value[__key] = _value

    def __call__(self, *args, **kwargs):
        pass
    
    def __str__(self):
        return f"DictAttr<{[_key for _key in self.__value.keys()]}>"
    
    def __repr__(self):
        return f"DictAttr<{[_key for _key in self.__value.keys()]}>"

    def to_dict(self) -> typing.Dict:
        return self.__value

    def to_string(self) -> str:
        return json.dumps(self.__value)
    
    def to_json_file(self, _filepath):
        if os.path.exists(_filepath):
            with open(_filepath, 'w') as _f:
                json.dump(self.__value, _f)
        else:
            # TODO: Raise File does not exists exception.
            raise Exception('File does not exists!')

class DictAttrList(DictAttr):
    """
        When the object is MutableSequence/List
    """
    def __init__(self, _list_obj:typing.List):
        """
            Initializing Object.
        """
        self.__value = _list_obj

    def __setitem__(self, _index, _value):
        if _index >= len(self.__value):
            # TODO: Raise Index out of bound exception.
            raise Exception("List assignment Index out of bound execption!")
        self.__value[_index] = _value

    def _get_value(self, _index):
        if _index >= len(self.__value):
            # TODO: Raise Index out of bound exception.
            raise Exception("Index out of bound execption!")
        return DictAttr(self.__value[_index])

    def __getitem__(self, _key):
        if isinstance(_key, slice):
            _start, _stop, _step = _key.indices(len(self))
            return DictAttr([self[i] for i in range(_start, _stop, _step)])
        elif isinstance(_key, int):
            return self._get_value(_key)
        else:
            # TODO: Raise Invalid type argument
            raise Exception('Invalid argument type: {}'.format(type(_key)))

    def __str__(self):
        _elem = "DictAttr<(...)>"
        return f"DictAttr<{[_elem for _ in self.__value]}>"
    
    def __repr__(self):
        _elem = "DictAttr<(...)>"
        return f"DictAttr<{[_elem for _ in self.__value]}>"

    def to_list(self) -> typing.List:
        return self.__value

    def to_string(self) -> str:
        return json.dumps(self.__value)
    
    def to_json_file(self, _filepath):
        if os.path.exists(_filepath):
            with open(_filepath, 'w') as _f:
                json.dump(self.__value, _f)
        else:
            # TODO: Raise File does not exists exception.
            raise Exception('File does not exists!')

# if __name__ == "__main__":
    # dattr_obj = DictAttr({
    #     "Dummy_Key": "Dummy_Data",
    #     "Dummy_List": [
    #         {
    #             "Dummy_Mapping": {
    #                 "keys_": "Dummy_Value_In_Mapping"
    #             }, 
    #             "Dummy_Flag":1
    #         }
    #     ]})
    # return DictAttr.from_string('{"Dummy_Key": "Dummy_Data","Dummy_List": [{"Dummy_Mapping": {"keys_": "Dummy_Value_In_Mapping"},"Dummy_Flag":100}]}')
    # print(dattr_obj.to_string())
    # print(dattr_obj.Dummy_List)
    # print(dattr_obj.Dummy_List[0].Dummy_Mapping.keys_)
    # print(dattr_obj.Dummy_List.to_list())
    # dattr_obj.Dummy_List[0] = 'Dummy_Replaced_Value'
    # print(dattr_obj.Dummy_List[0])
    # print(dattr_obj.to_string())
    # print(dattr_obj.Dummy_Mapping.keys())