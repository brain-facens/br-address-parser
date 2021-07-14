import json
import logging

import pytest

from br_address_parser import parse, sanitize_address


@pytest.mark.parametrize(
    "address_with_spaces,expected",
    [
        (
            "RUA  DA  GROELANDIA,    1.554B,-APTO. 104B03 -,BAIRRO",
            "RUA DA GROELANDIA , 1554 B - APTO 104 B 03 - BAIRRO",
        ),
        (
            "R SILVIO ROMERO-8-AP 504 - SANTA TERESA - RIO DE JANEIRO - RJ",
            "R SILVIO ROMERO - 8 - AP 504 - SANTA TERESA - RIO DE JANEIRO - RJ",
        ),
        (
            "RUA  DA  GROELANDIA,    1.554 -  - BAIRRO",
            "RUA DA GROELANDIA , 1554 - BAIRRO",
        ),
    ],
)
def test_sanite_address(address_with_spaces: str, expected: dict):
    actual = sanitize_address(address_with_spaces)
    assert actual == expected


def test_parse_with_empty_fields():
    address = "AV ANAVILLE 1-QD 3 LT 4 - RESIDENCIAL ANAVILLE - ANAPOLIS - GO"
    actual = parse(address, {"number": "S/N"})

    expected = {
        "street": "AV ANAVILLE 1",
        "number": "S/N",
        "complement": "QD 3 LT 4",
        "neighborhood": "RESIDENCIAL ANAVILLE",
        "city": "ANAPOLIS",
        "state": "GO",
    }

    for key, vaue in expected.items():
        assert (
            expected[key] == actual[key]
        ), "Expected value {} for key {}, but received {}".format(
            expected[key], key, actual[key]
        )


@pytest.fixture
def addresses():
    data_path = "tests/addresses.json"
    data = json.loads(open(data_path, "r").read())
    return data


def test_parse(addresses):
    for test in addresses:
        if test["expected"]:
            actual = parse(test["address"])
            for key, value in test["expected"].items():
                assert (
                    test["expected"][key] == actual[key]
                ), "Expected value {} for key {}, received {}".format(
                    test["expected"][key], key, actual[key]
                )
        else:
            actual = parse(test["address"])
            assert actual is None
