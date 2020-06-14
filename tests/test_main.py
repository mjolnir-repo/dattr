import pytest
import json
import traceback
import sys
import os
from dattr.main import DictAttr


@pytest.fixture(name="source_data_str", scope="module")
def _source_data_str(source_data):
    """
        Source data in string format.
    """
    return json.dumps(source_data)

@pytest.fixture(name="dattr_obj", scope="module")
def _dattr_obj(source_data):
    """
        Creating DictAttr object.
    """
    try:
        return DictAttr(source_data)
    except Exception as e:
        print("~" * 100)
        traceback.print_exc(file=sys.stdout)
        print("~" * 100)


def test_from_string(source_data_str, dattr_obj):
    """ Testing alternate constructor `from_string()`. """
    try:
        assert DictAttr.from_string(source_data_str) == dattr_obj
    except Exception as e:
        print("~" * 100)
        traceback.print_exc(file=sys.stdout)
        print("~" * 100)
        assert False

def test_from_json_file(source_file, source_data, dattr_obj):
    """ Testing alternate constructor `from_json_file()`. """
    try:
        assert DictAttr.from_json_file(source_file) == dattr_obj
    except Exception as e:
        print("~" * 100)
        traceback.print_exc(file=sys.stdout)
        print("~" * 100)
        assert False

def test_traverse_via_interpolation(dattr_obj):
    """ Testing support for interpolation syntax while extracting data. """
    assert dattr_obj["Dummy_Key"] == "Dummy_Data"
    assert dattr_obj["Dummy_List"][0]["Dummy_Flag"] == 2
    assert dattr_obj["Dummy_List"][0]["Dummy_Mapping"]["keys"] == "Dummy_Value_In_Mapping"

def test_traverse_via_dot_notation(dattr_obj):
    """ Testing support for dot notation syntax while extracting data. """
    assert dattr_obj.Dummy_Key == "Dummy_Data"
    assert dattr_obj.Dummy_List[0].Dummy_Flag == 2

def test_traverse_via_dot_notation_caveat(dattr_obj):
    """ Testing caveate for dot notation syntax while extracting data. """
    with pytest.raises(AssertionError):
        assert dattr_obj.Dummy_List[0].Dummy_Mapping.keys == "Dummy_Value_In_Mapping"
    assert dattr_obj.Dummy_List[0].Dummy_Mapping['keys'] == "Dummy_Value_In_Mapping"

def test_comparison_operations(dattr_obj):
    """ Testing comparison capabilities. """
    assert dattr_obj.Dummy_List[0].Dummy_Flag == 2
    assert not dattr_obj.Dummy_List[0].Dummy_Flag == 1
    assert dattr_obj.Dummy_List[0].Dummy_Flag < 3
    assert not dattr_obj.Dummy_List[0].Dummy_Flag < 2
    assert dattr_obj.Dummy_List[0].Dummy_Flag <= 3
    assert dattr_obj.Dummy_List[0].Dummy_Flag <= 2
    assert not dattr_obj.Dummy_List[0].Dummy_Flag <= 1
    assert dattr_obj.Dummy_List[0].Dummy_Flag >= 2
    assert dattr_obj.Dummy_List[0].Dummy_Flag >= 1
    assert not dattr_obj.Dummy_List[0].Dummy_Flag >= 3
    assert dattr_obj.Dummy_List[0].Dummy_Flag > 1
    assert not dattr_obj.Dummy_List[0].Dummy_Flag > 2

def test_data_assignment_via_interpolation(dattr_obj):
    """ Testing support for interpolation syntax while assigning data. """
    dattr_obj.Dummy_List[0].Dummy_Mapping['Another_Key'] = 'Dummy_Replaced_Value'
    assert dattr_obj.Dummy_List[0].Dummy_Mapping.Another_Key == 'Dummy_Replaced_Value'

def test_data_assignment_via_dot_notation(dattr_obj):
    """ Testing support for dot notation syntax while assigning data. """
    dattr_obj.Dummy_List[0].Dummy_Mapping.Another_Key = 'Dummy_Another_Value'
    assert dattr_obj.Dummy_List[0].Dummy_Mapping['Another_Key'] == 'Dummy_Another_Value'

def test_dictionary_behaviour(dattr_obj, source_data):
    """ Testing support for built-in dictionary features like keys() method. """
    assert dattr_obj.keys() == source_data.keys()

def test_to_json_file(dattr_obj, target_file, source_data):
    """ Testing `to_json_file()` feature. """
    dattr_obj.to_json_file(target_file)
    assert os.path.exists(target_file)
    with open(target_file, 'r') as f:
        assert json.load(f) == source_data
