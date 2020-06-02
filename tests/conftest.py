import pytest
import json
import os
import sys
import traceback


@pytest.yield_fixture(name="test_file_dir", scope="module")
def _test_file_dir():
    _dir = ".test_bed"
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    yield ".test_bed"
    os.rmdir(_dir)


@pytest.fixture(name="source_file_name", scope="module")
def _source_file_name():
    return 'dummy_source_file.json'


@pytest.fixture(name="source_data", scope="module")
def _source_data():
    return {
        "Dummy_Key": "Dummy_Data",
        "Dummy_List": [
            {
                "Dummy_Mapping": {
                    "keys": "Dummy_Value_In_Mapping"
                }, 
                "Dummy_Flag":2
            }
        ]}


@pytest.yield_fixture(name="source_file", scope="module", autouse=True)
def _source_file(test_file_dir, source_file_name, source_data):
    """ 
        Creating JSON file to test alternate constructor - `from_json()`
    """
    try:
        source_file = os.path.join(test_file_dir, source_file_name)
        with open(source_file, 'w') as f:
            json.dump(source_data, f)
        yield source_file
        os.remove(source_file)
    except Exception as e:
        print("~" * 100)
        traceback.print_exc(file=sys.stdout)
        print("~" * 100)
        assert False


@pytest.fixture(name="target_file_name", scope="module")
def _target_file_name():
    return 'dummy_target_file.json'


@pytest.yield_fixture(name="target_file", scope="module", autouse=True)
def _target_file(test_file_dir, target_file_name):
    """ 
        Creating JSON file name to test `to_json()`
    """
    try:
        target_file = os.path.join(test_file_dir, target_file_name)
        yield target_file
        if os.path.exists(target_file):
            os.remove(target_file)
    except Exception as e:
        print("~" * 100)
        traceback.print_exc(file=sys.stdout)
        print("~" * 100)
        assert False