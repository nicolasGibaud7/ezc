import json
import os
from configparser import ConfigParser
from typing import Any, Dict, List

import pytest
from ezc.cli import (
    _add_ingredient,
    _add_ingredients,
    _add_recipe,
    _create_list,
)

from data.data_test_public_api import (
    data_add_ingredient,
    data_add_ingredients,
    data_add_recipe,
    data_create_list,
)


@pytest.mark.parametrize(
    "name, shelf, price, category, unite, expected_result", data_add_ingredient
)
def test_add_ingredient(
    name: str,
    shelf: str,
    price: float,
    category: str,
    unite: str,
    expected_result: Dict[str, Any],
):
    configuration = ConfigParser()
    configuration.read("test_config.ini")
    ingredient_database = configuration.get("CONFIG", "INGREDIENTS_DATABASE")
    with open(ingredient_database, "r") as json_file:
        original_json_content = json.load(json_file)
    try:
        _add_ingredient(name, shelf, price, category, unite, configuration)
        with open(ingredient_database, "r") as json_file:
            json_content = json.load(json_file)
        assert expected_result in json_content
    finally:
        with open(ingredient_database, "w") as json_file:
            json.dump(original_json_content, json_file)


@pytest.mark.parametrize(
    "excel_filename, expected_result", data_add_ingredients
)
def test_add_ingredients(
    excel_filename: str, expected_result: List[Dict[str, Any]]
):
    configuration = ConfigParser()
    configuration.read("test_config.ini")
    ingredient_database = configuration.get("CONFIG", "INGREDIENTS_DATABASE")
    with open(ingredient_database, "r") as json_file:
        original_json_content = json.load(json_file)
    try:
        _add_ingredients(excel_filename, configuration)
        with open(ingredient_database, "r") as json_file:
            json_content = json.load(json_file)
        for ingredient in expected_result:
            assert ingredient in json_content
    finally:
        with open(ingredient_database, "w") as json_file:
            json.dump(original_json_content, json_file)


@pytest.mark.parametrize("excel_filename, expected_result", data_add_recipe)
def test_add_recipe(excel_filename: str, expected_result: Dict[str, Any]):
    configuration = ConfigParser()
    configuration.read("test_config.ini")
    recipes_database = configuration.get("CONFIG", "RECIPES_DATABASE")

    with open(recipes_database, "r") as json_file:
        original_json_content = json.load(json_file)
    try:
        _add_recipe(excel_filename, configuration)
        with open(recipes_database, "r") as json_file:
            json_content = json.load(json_file)
            assert expected_result in json_content
    finally:
        with open(recipes_database, "w") as json_file:
            json.dump(original_json_content, json_file)


@pytest.mark.parametrize(
    "recipes, expected_result, expected_result_frozen, expected_result_market, expected_result_supermarket",
    data_create_list,
)
def test_create_list(
    recipes: List[str],
    expected_result: List[Dict[str, Any]],
    expected_result_frozen: List[Dict[str, Any]],
    expected_result_market: List[Dict[str, Any]],
    expected_result_supermarket: List[Dict[str, Any]],
):
    configuration = ConfigParser()
    configuration.read("test_config.ini")

    try:
        shopping_list = _create_list(recipes, configuration, False)
        for ingredient in expected_result:
            assert ingredient in shopping_list.to_json()

        assert shopping_list.frozen_food.to_json() == expected_result_frozen
        assert shopping_list.market.to_json() == expected_result_market
        assert (
            shopping_list.supermarket.to_json() == expected_result_supermarket
        )

    finally:
        try:
            os.remove("shopping_list.xlsx")
        except OSError:
            print("Can't remove shopping_list.xlsx file")
