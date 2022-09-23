import json
from typing import Any, Dict

import pytest
from ezc.exceptions import IngredientNotFoundException, RecipeNotFoundException
from ezc.json_utility import (
    add_ingredient_to_json_file,
    add_ingredients_to_json_file,
    add_recipe_to_json_file,
    check_ingredient_presence,
    check_recipe_presence,
    get_json_ingredient,
    get_json_recipe,
    update_ingredient_in_json_file,
    update_ingredients_in_json_file,
)
from tests.test_json_utility.data.data_test_public_json import (
    data_add_ingredient_to_json_file,
    data_add_ingredients_to_json_file,
    data_add_recipe_to_json_file,
    data_check_ingredient_presence,
    data_check_recipe_presence,
    data_get_json_ingredient,
    data_get_json_recipe,
    data_update_ingredient_in_json_file,
    data_update_ingredients_in_json_file,
)


@pytest.mark.parametrize(
    "json_filename, name, shelf, price, unite, expected_result",
    data_add_ingredient_to_json_file,
)
def test_add_ingredient_to_json_file(
    json_filename, name, shelf, price, unite, expected_result
):
    with open(json_filename, "r") as json_file:
        original_json_content = json.load(json_file)

    add_ingredient_to_json_file(json_filename, name, shelf, price, unite)
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result

    with open(json_filename, "w") as json_file:
        json.dump(original_json_content, json_file)


@pytest.mark.parametrize(
    "json_filename, ingredients_attributes_value, expected_result",
    data_add_ingredients_to_json_file,
)
def test_add_ingredients_to_json_file(
    json_filename, ingredients_attributes_value, expected_result
):
    with open(json_filename, "r") as json_file:
        original_json_content = json.load(json_file)

    add_ingredients_to_json_file(json_filename, ingredients_attributes_value)
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result

    with open(json_filename, "w") as json_file:
        json.dump(original_json_content, json_file)


@pytest.mark.parametrize(
    "json_filename, ingredients_attributes_value, expected_result",
    data_update_ingredients_in_json_file,
)
def test_update_ingredients_in_json_file(
    json_filename, ingredients_attributes_value, expected_result
):
    with open(json_filename, "r") as json_file:
        original_json_content = json.load(json_file)

    update_ingredients_in_json_file(
        json_filename, ingredients_attributes_value
    )
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result

    with open(json_filename, "w") as json_file:
        json.dump(original_json_content, json_file)


@pytest.mark.parametrize(
    "json_filename, name, shelf, price, unite, expected_result",
    data_update_ingredient_in_json_file,
)
def test_update_ingredient_in_json_file(
    json_filename, name, shelf, price, unite, expected_result
):
    with open(json_filename, "r") as json_file:
        original_json_content = json.load(json_file)

    update_ingredient_in_json_file(json_filename, name, shelf, price, unite)
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result

    with open(json_filename, "w") as json_file:
        json.dump(original_json_content, json_file)


@pytest.mark.parametrize(
    "json_filename, recipe_name, ingredients_list, expected_result",
    data_add_recipe_to_json_file,
)
def test_add_recipe_to_json_file(
    json_filename, recipe_name, ingredients_list, expected_result
):
    with open(json_filename, "r") as json_file:
        original_json_content = json.load(json_file)

    add_recipe_to_json_file(json_filename, recipe_name, ingredients_list)
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)

    with open(json_filename, "w") as json_file:
        json.dump(original_json_content, json_file)

    assert json_content == expected_result


@pytest.mark.parametrize("recipe_name, expected_result", data_get_json_recipe)
def test_get_json_recipe(recipe_name: str, expected_result):
    try:
        assert get_json_recipe(recipe_name) == expected_result
    except RecipeNotFoundException:
        assert expected_result is None


@pytest.mark.parametrize(
    "recipe_name, expected_result", data_check_recipe_presence
)
def test_check_recipe_presence(recipe_name: str, expected_result):
    assert check_recipe_presence(recipe_name) == expected_result


@pytest.mark.parametrize(
    "recipe_name, expected_result", data_check_ingredient_presence
)
def test_check_ingredient_presence(recipe_name: str, expected_result):
    assert check_ingredient_presence(recipe_name) == expected_result


@pytest.mark.parametrize(
    "ingredient_name, expected_result", data_get_json_ingredient
)
def test_get_json_ingredient(
    ingredient_name: str, expected_result: Dict[str, Any]
):
    try:
        assert get_json_ingredient(ingredient_name) == expected_result
    except IngredientNotFoundException:
        assert expected_result is None
