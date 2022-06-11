import json
from typing import Any, Dict, List

from src.constants import (
    INGREDIENTS_DATABASE_FILENAME,
    RECIPE_DATABASE_FILENAME,
)
from src.globals import logger
from src.utility import format_option


def get_json_ingredient(ingredient_name: str) -> Dict[str, Any]:
    ingredients = []
    with open(INGREDIENTS_DATABASE_FILENAME, "r") as ingredients_file:
        ingredients = json.load(ingredients_file)
    for ingredient in ingredients:
        if ingredient["name"] == ingredient_name:
            return ingredient
    raise Exception(
        f"Ingredient {ingredient_name} not found"
    )  # TODO Raise IngredientNotFoundException instead


def check_ingredient_presence(ingredient_name: str) -> bool:
    return _check_json_element_presence(
        ingredient_name, "name", INGREDIENTS_DATABASE_FILENAME
    )


def check_recipe_presence(recipe_name: str) -> bool:
    return _check_json_element_presence(
        recipe_name, "name", RECIPE_DATABASE_FILENAME
    )


def get_json_recipe(recipe_name: str) -> Dict[str, Any]:
    recipes = []
    with open(RECIPE_DATABASE_FILENAME, "r") as recipes_file:
        recipes = json.load(recipes_file)
    for recipe in recipes:
        if recipe["name"] == recipe_name:
            return recipe
    raise Exception(
        f"Recipe {recipe_name} not found"
    )  # TODO Raise RecipeNotFoundException instead


def add_recipe_to_json_file(
    json_filename: str,
    recipe_name: str,
    ingredients_list: List[Dict[str, Any]],
):
    # Construct a dict object which contains the recipe name and an ingredients list
    recipe_element = {
        "name": recipe_name,
        "ingredients_list": ingredients_list,
    }

    # Add it to the json file
    _add_json_element_to_json_file(json_filename, recipe_element)


def update_ingredient_in_json_file(
    name: str, shelf: str, price: float, unite: str
):
    name, shelf, price, unite = map(format_option, [name, shelf, price, unite])
    ingredient_element = {
        "name": name,
        "shelf": shelf,
        "price": price,
        "unite": unite,
    }
    _update_element_in_json_file(
        INGREDIENTS_DATABASE_FILENAME, ingredient_element, "name"
    )


def update_ingredients_in_json_file(
    ingredients_attributes_values: List[List[Any]],
):
    for ingredient_attribute_value in ingredients_attributes_values:
        name, shelf, price, unite = ingredient_attribute_value
        json_ingredient_representation = {
            "name": name,
            "shelf": shelf,
            "price": price,
            "unite": unite,
        }
        _update_element_in_json_file(
            INGREDIENTS_DATABASE_FILENAME,
            json_ingredient_representation,
            "name",
        )


def add_ingredients_to_json_file(
    json_filename: str, ingredients_attributes_value: List[Any]
):
    json_ingredients_representation = []
    for ingredient in ingredients_attributes_value:
        name, shelf, price, unite = ingredient
        json_ingredients_representation.append(
            {"name": name, "shelf": shelf, "price": price, "unite": unite}
        )
    _add_json_elements_to_json_file(
        json_filename, json_ingredients_representation
    )


def add_ingredient_to_json_file(
    json_filename: str,
    name: str,
    shelf: str,
    price: float,
    unite: str,
):
    name, shelf, price, unite = map(format_option, [name, shelf, price, unite])
    ingredient_element = {
        "name": name,
        "shelf": shelf,
        "price": price,
        "unite": unite,
    }
    _add_json_element_to_json_file(json_filename, ingredient_element)


def _add_json_element_to_json_file(
    json_filename: str, element: Dict[str, Any]
):

    json_content = _get_json_content_with_added_element(json_filename, element)

    with open(json_filename, "w") as json_file:
        json.dump(json_content, json_file)


def _add_json_elements_to_json_file(
    json_filename: str, elements: List[Dict[str, Any]]
):
    json_content = _get_json_content_with_added_elements(
        json_filename, elements
    )

    with open(json_filename, "w") as json_file:
        json.dump(json_content, json_file)


def _get_json_content_with_added_element(
    json_filename: str, element: Dict[str, Any]
) -> str:
    # TODO add verification if the element is already in the json file
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
        json_content.append(element)
        logger.debug(json_content)
    return json_content


def _get_json_content_with_added_elements(
    json_filename: str, elements: List[Dict[str, Any]]
) -> str:
    # TODO add verification if one of the element is already in the json file
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
        for element in elements:
            json_content.append(element)
        logger.debug(json_content)
    return json_content


def _check_json_element_presence(
    element_identifier: Any, identifier_attribute: str, json_filename: str
) -> bool:
    json_content = []
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    return any(
        [
            element
            for element in json_content
            if element[identifier_attribute] == element_identifier
        ]
    )


def _update_element_in_json_file(
    json_filename: str, new_element: Dict[str, Any], identifier_attribute: str
):
    json_content = []
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    for index, element in enumerate(json_content):
        if element[identifier_attribute] == new_element[identifier_attribute]:
            json_content[index] = new_element
    with open(json_filename, "w") as json_file:
        json.dump(json_content, json_file)
