"""
This test module has tests relating to parser classes
"""
import os

import pytest

import pygaps


@pytest.mark.parsing
class TestJson(object):
    def test_isotherm_to_json(self, basic_isotherm):
        """Tests the parsing of an isotherm to json"""

        test_isotherm_json = pygaps.isotherm_to_json(basic_isotherm)
        new_isotherm = pygaps.isotherm_from_json(test_isotherm_json)

        assert basic_isotherm == new_isotherm

    def test_pointisotherm_to_json(self, basic_pointisotherm):
        """Tests the parsing of an isotherm to json"""

        test_isotherm_json = pygaps.isotherm_to_json(basic_pointisotherm)
        new_isotherm = pygaps.isotherm_from_json(test_isotherm_json)

        assert basic_pointisotherm == new_isotherm

        return

    def test_isotherm_from_json_nist(self):

        JSON_PATH_NIST = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'docs', 'examples', 'data', 'parsing', 'nist', 'nist_iso.json')

        with open(JSON_PATH_NIST) as file:
            pygaps.isotherm_from_json(file.read(), fmt='NIST')

        return

    def test_isotherm_to_json_nist(self):

        JSON_PATH_NIST = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'docs', 'examples', 'data', 'parsing', 'nist', 'nist_iso.json')

        with open(JSON_PATH_NIST) as file:
            json_str = file.read()

        isotherm = pygaps.isotherm_from_json(json_str, fmt='NIST')

        new_json_str = pygaps.isotherm_to_json(isotherm, fmt='NIST')

        return new_json_str
