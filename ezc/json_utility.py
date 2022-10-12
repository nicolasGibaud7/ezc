import json
from typing import Any, Dict, List

from ezc.constants import (
    INGREDIENTS_DATABASE_FILENAME,
    RECIPE_DATABASE_FILENAME,
)
from ezc.exceptions import IngredientNotFoundException, RecipeNotFoundException
from ezc.globals import logger


def get_json_ingredient(ingredient_name: str) -> Dict[str, Any]:
    """Find and return specified ingredient description in json database

    Args:
        ingredient_name (str): Ingredient name to search

    Raises:
        Exception: _description_

    Returns:
        Dict[str, Any]: _description_
    """
    ingredients = []
    with open(INGREDIENTS_DATABASE_FILENAME, "r") as ingredients_file:
        ingredients = json.load(ingredients_file)
    for ingredient in ingredients:
        if (
            ingredient["name"] == ingredient_name
        ):  # TODO Create a private method which will search elements in json files
            return ingredient
    raise IngredientNotFoundException(
        f"Ingredient {ingredient_name} not found"
    )


def check_ingredient_presence(
    ingredient_name: str, json_database: str
) -> bool:
    """Check an ingredient presence in ingredients json database

    Args:
        ingredient_name (str): Name of the ingredient to check the presence

    Returns:
        bool: True if searched recipe is in recipes json database else False
    """
    return _check_json_element_presence(ingredient_name, "name", json_database)


def check_recipe_presence(recipe_name: str) -> bool:
    """Check a recipe presence in recipes json database

    Args:
        recipe_name (str): Name of the recipe to check the presence

    Returns:
        bool: True if searched recipe is in recipes json database else False
    """
    return _check_json_element_presence(
        recipe_name, "name", RECIPE_DATABASE_FILENAME
    )


def get_json_recipe(recipe_name: str) -> Dict[str, Any]:
    """Find and return json recipe representation with the recipe name in entry

    Args:
        recipe_name (str): Name of the recipe to search

    Raises:
        Exception: Recipe name isn't in the json database

    Returns:
        Dict[str, Any]: Searched recipe json representation
    """
    recipes = []
    with open(RECIPE_DATABASE_FILENAME, "r") as recipes_file:
        recipes = json.load(recipes_file)
    for recipe in recipes:
        if (
            recipe["name"] == recipe_name
        ):  # TODO Create a private method which will search elements in json files
            return recipe
    raise RecipeNotFoundException(f"Recipe {recipe_name} not found")


def add_recipe_to_json_file(
    json_filename: str,
    recipe_name: str,
    ingredients_list: List[Dict[str, Any]],
):
    """Add a recipe description to a json file

    Args:
        json_filename (str): Json file name
        recipe_name (str): Recipe name
        ingredients_list (List[Dict[str, Any]]): List of recipe ingredients
        and their quantity
    """
    recipe_element = {
        "name": recipe_name,
        "ingredients_list": ingredients_list,
    }

    _add_json_element_to_json_file(json_filename, recipe_element)


def update_ingredient_in_json_file(
    json_filename: str, ingredient_attributes: Dict[str, Any]
):
    """Update ingredient attributes in json file

    Args:
        ingredient_attributes (Dict[str, Any]): Ingredient attributes
    """
    _update_element_in_json_file(json_filename, ingredient_attributes, "name")


def update_ingredients_in_json_file(
    json_filename: str, ingredients_attributes_values: List[List[Any]]
):
    """Update ingredients attributes in json file

    Args:
        ingredients_attributes_values (List[List[Any]]): List of ingredient attributes list
    """
    for ingredient_attribute_value in ingredients_attributes_values:
        name, shelf, price, category, unite = ingredient_attribute_value
        json_ingredient_representation = {
            "name": name,
            "shelf": shelf,
            "price": price,
            "category": category,
            "unite": unite,
        }
        _update_element_in_json_file(
            json_filename, json_ingredient_representation, "name"
        )


def add_ingredients_to_json_file(
    json_filename: str, ingredients_attributes_value: List[List[Any]]
):
    """Add ingredients json representation to a json file

    Args:
        json_filename (str): Json file name
        ingredients_attributes_value (List[List[Any]]): List of ingredient attributes list
    """
    json_ingredients_representation = []
    for ingredient in ingredients_attributes_value:
        name, shelf, price, category, unite = ingredient
        json_ingredients_representation.append(
            {
                "name": name,
                "shelf": shelf,
                "price": price,
                "category": category,
                "unite": unite,
            }
        )
    _add_json_elements_to_json_file(
        json_filename, json_ingredients_representation
    )


def add_ingredient_to_json_file(
    json_filename: str, ingredient_attributes: Dict[str, Any]
):
    """Add ingredient json representation to a json file

    Args:
        json_filename (str): Json file name
        ingredient_attributes (Dict[str, Any]): Ingredient info dictionary
    """
    _add_json_element_to_json_file(json_filename, ingredient_attributes)


def _add_json_element_to_json_file(
    json_filename: str, element: Dict[str, Any]
):
    """Add a json formatted element to a json file

    Args:
        json_filename (str): Name of the json file
        elements (List[Dict[str, Any]]): Json element to add to the json file
    """

    json_content = _get_json_content_file_with_added_element(
        json_filename, element
    )
    print(json_content)

    with open(json_filename, "w") as json_file:
        json.dump(json_content, json_file, indent=4)


def _add_json_elements_to_json_file(
    json_filename: str, elements: List[Dict[str, Any]]
):
    """Add json multiple formatted elements to a json file

    Args:
        json_filename (str): Name of the json file
        elements (List[Dict[str, Any]]): Json elements to add to the json file
    """
    json_content = _get_json_content_file_with_added_elements(
        json_filename, elements
    )

    with open(json_filename, "w") as json_file:
        json.dump(json_content, json_file, indent=4)


def _get_json_content_file_with_added_element(
    json_filename: str, element: Dict[str, Any]
) -> str:
    """Return a json content with an added element

    Args:
        json_filename (str): Name of the json file
        element (Dict[str, Any]): Element to add to the json content

    Returns:
        str: Json content file with the added element
    """
    # TODO add verification if the element is already in the json file
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
        json_content.append(element)
        logger.debug(json_content)
    return json_content


def _get_json_content_file_with_added_elements(
    json_filename: str, elements: List[Dict[str, Any]]
) -> str:
    """Return a json content with added elements

    Args:
        json_filename (str): Name of the json file
        elements (List[Dict[str, Any]]): Elements to add to json content

    Returns:
        str: Json content file with added elements
    """
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
    """Check any element presence in json file

    Args:
        element_identifier (Any): Value of element identifier attribute
        identifier_attribute (str): Element attribute type which permit to identify it
        json_filename (str): Json file to check

    Returns:
        bool: True if element is in json file else False
    """
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
    """Replace json element by its updated version

    Args:
        json_filename (str): Json file
        new_element (Dict[str, Any]): New json element
        identifier_attribute (str): Attribute which will permit to identify json element to update
    """
    json_content = []
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    for index, element in enumerate(json_content):
        if element[identifier_attribute] == new_element[identifier_attribute]:
            json_content[index] = new_element
    with open(json_filename, "w") as json_file:
        json.dump(json_content, json_file, indent=4)
