from typing import Any, Dict, List

import pytest
from ezc.recipes import Ingredient, Recipe, RecipeElement
from ezc.utility import format_option
from tests.test_recipes.data.data_test_recipes import (
    data_test_ingredient,
    data_test_recipe,
    data_test_recipe_element,
)


@pytest.mark.parametrize(
    "name, shelf, price, unite, expected_result", data_test_ingredient
)
def test_ingredient(
    name: str,
    shelf: str,
    price: float,
    unite: str,
    expected_result: Dict[str, Any],
):
    ingredient = Ingredient(name, shelf, price, unite)
    assert ingredient.name == format_option(name)
    assert ingredient.shelf == format_option(shelf)
    assert ingredient.price == format_option(price)
    assert ingredient.unite == format_option(unite)
    assert ingredient.to_json() == expected_result


@pytest.mark.parametrize(
    "ingredient, quantity, expected_result", data_test_recipe_element
)
def test_recipe_element(
    ingredient: Ingredient,
    quantity: int,
    expected_result: Dict[str, Any],
):

    recipe_element = RecipeElement(ingredient, quantity)
    assert recipe_element.ingredient.name == format_option(ingredient.name)
    assert recipe_element.ingredient.shelf == format_option(ingredient.shelf)
    assert recipe_element.ingredient.price == format_option(ingredient.price)
    assert recipe_element.ingredient.unite == format_option(ingredient.unite)
    assert recipe_element.quantity == format_option(quantity)
    assert recipe_element.to_json() == expected_result


@pytest.mark.parametrize(
    "name, ingredients, expected_result", data_test_recipe
)
def test_recipe(
    name: str,
    ingredients: List[RecipeElement],
    expected_result: Dict[str, Any],
):

    recipe = Recipe(name, ingredients)
    assert recipe.name == format_option(name)
    for recipe_ingredient, ingredient in zip(recipe.ingredients, ingredients):
        assert recipe_ingredient == ingredient
    assert recipe.to_json() == expected_result
