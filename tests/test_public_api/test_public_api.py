import json

import pytest
from ezc.cli import add_ingredient
from ezc.constants import INGREDIENTS_DATABASE_FILENAME

from data.data_test_public_api import data_add_ingredient


@pytest.mark.parametrize(
    "name, shelf, price, unite, expected_result", data_add_ingredient
)
def test_add_ingredient(
    name: str,
    shelf: str,
    price: float,
    unite: str,
    expected_result: str,
):
    with open(INGREDIENTS_DATABASE_FILENAME, "r") as json_file:
        original_json_content = json.load(json_file)
    add_ingredient(name, shelf, price, unite, False)
    with open(INGREDIENTS_DATABASE_FILENAME, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result
    with open(INGREDIENTS_DATABASE_FILENAME, "w") as json_file:
        json.dump(original_json_content, json_file)
