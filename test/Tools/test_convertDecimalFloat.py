# test_convert_decimal.py
import pytest
from decimal import Decimal
from Tools.convertDecimalFloat import convertDecimalFloat  # Asegúrate de importar la función desde el módulo correcto

def test_convert_single_decimal():
    assert convertDecimalFloat(Decimal('10.5')) == 10.5

def test_convert_list_of_decimals():
    input_data = [Decimal('1.1'), Decimal('2.2'), Decimal('3.3')]
    expected_output = [1.1, 2.2, 3.3]
    assert convertDecimalFloat(input_data) == expected_output

def test_convert_nested_dict():
    input_data = {
        'a': Decimal('4.5'),
        'b': {
            'c': Decimal('6.7'),
            'd': [Decimal('8.9'), Decimal('10.11')]
        }
    }
    expected_output = {
        'a': 4.5,
        'b': {
            'c': 6.7,
            'd': [8.9, 10.11]
        }
    }
    assert convertDecimalFloat(input_data) == expected_output

def test_convert_mixed_data():
    input_data = {
        'value': Decimal('3.14'),
        'list': [Decimal('1.618'), 'not_a_decimal', {'inner': Decimal('2.718')}]
    }
    expected_output = {
        'value': 3.14,
        'list': [1.618, 'not_a_decimal', {'inner': 2.718}]
    }
    assert convertDecimalFloat(input_data) == expected_output

def test_convert_empty_data():
    assert convertDecimalFloat([]) == []
    assert convertDecimalFloat({}) == {}
    assert convertDecimalFloat('just_a_string') == 'just_a_string'


