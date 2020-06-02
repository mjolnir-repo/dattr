import pytest
import json


def test_dummy(source_file):
    with open(source_file, 'r') as f:
        print(json.load(f))
    assert True