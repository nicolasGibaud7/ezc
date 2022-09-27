from typing import Any, List

import click

from ezc.constants import (
    INGREDIENT_TYPE,
    INGREDIENTS_CATEGORIES,
    INGREDIENTS_DATABASE_FILENAME,
    RECIPE_DATABASE_FILENAME,
    RECIPE_TYPE,
    RECIPES_CATEGORIES,
    SHELF_LIST,
    SHOPPING_LIST_CATEGORIES,
    SHOPPING_LIST_TYPE,
    TABLE_TYPE_LIST,
)
from ezc.excel_factory import ExcelFactory
from ezc.exceptions import IngredientNotFoundException, RecipeNotFoundException
from ezc.globals import logger
from ezc.json_utility import (
    add_ingredient_to_json_file,
    add_ingredients_to_json_file,
    add_recipe_to_json_file,
    check_ingredient_presence,
    get_json_ingredient,
    get_json_recipe,
    update_ingredient_in_json_file,
    update_ingredients_in_json_file,
)
from ezc.recipes import Ingredient, Recipe, RecipeElement
from ezc.utility import format_option, print_shopping_list


@click.group()
def cli():
    pass


@cli.command()
@click.argument("recipes", nargs=-1)
@click.option("-l", "--log", type=bool, required=False, default=False)
def create_list(recipes: List[str], log: bool):
    logger.set_log_activation(log)
    return _create_list(recipes, log)


@cli.command()
@click.option("-n", "--name", type=str, required=True)
@click.option("-s", "--shelf", type=click.Choice(SHELF_LIST), required=True)
@click.option("-p", "--price", type=float, required=True)
@click.option("-u", "--unite", type=str, required=False, default="kg")
@click.option("-l", "--log", type=bool, required=False, default=False)
def add_ingredient(name: str, shelf: str, price: float, unite: str, log: bool):
    """Add an individual ingredient to the json database by passing all ingredient info

    Args:
        name (str): Ingredient name
        shelf (str): Ingredient shelf
        price (float): Ingredient price
        unite (str): Ingredient unite
        log (bool): Is log activated or not
    """
    logger.set_log_activation(log)
    _add_ingredient(name, shelf, price, unite)


@cli.command()
@click.argument("excel_filename", type=click.Path(exists=True))
@click.option("--log / --no-log", required=False, default=False)
def add_ingredients(excel_filename: str, log: bool):
    """Add a group of ingredients described in a dedicated excel file
    to json ingredient database

    Args:
        excel_filename (str): Ingredients description
        log (bool): Is log activated or not
    """
    logger.set_log_activation(log)
    _add_ingredients(excel_filename)


@cli.command()
@click.argument("excel_filename", type=click.Path(exists=True))
@click.option("-l", "--log", type=bool, required=False, default=False)
def add_recipe(excel_filename: str, log: bool):
    """Add a recipe to json recipe database based on a recipe description
    in an excel file

    Args:
        excel_filename (str): Recipe description
        log (bool): Is log activated or not
    """
    logger.set_log_activation(log)
    _add_recipe(excel_filename)


@cli.command()
@click.option("-n", "--name", type=str, default="table.xlsx")
@click.option("-t", "--table_type", type=click.Choice(TABLE_TYPE_LIST))
@click.option("-l", "--log", type=bool, required=False, default=False)
def create_table(name: str, table_type: str, log: bool):
    create_excel_table(name, table_type, log)


def _create_list(recipes: List[str], log: bool) -> List[Any]:
    """Create a shopping list based on recipes list

    Args:
        recipes (List[str]): Recipes list to follow to create shopping list

    Returns:
        _type_: _description_
    """
    shopping_list = []
    logger.debug(
        f"Creating shopping list for {len(recipes)} recipes : {' - '.join(recipes)}"
    )
    for recipe_name in recipes:
        logger.debug(f"Adding {recipe_name} recipe ingredients")
        try:
            recipe_element = get_json_recipe(recipe_name)
        except RecipeNotFoundException:
            logger.error(
                f"Recipe {recipe_name} is not in the recipes database. Please add it."
            )
            continue

        ingredients = recipe_element["ingredients_list"]
        for ingredient in ingredients:
            ingredient_name = ingredient["ingredient_name"]
            quantity = ingredient["quantity"]
            logger.debug(f"Adding {quantity} {ingredient_name} ingredient")
            try:
                ingredient_element = get_json_ingredient(ingredient_name)
            except IngredientNotFoundException:
                logger.error(
                    f"Ingredient {ingredient_name} is not in the ingredients database"
                )
                continue

            shopping_element = {
                "name": ingredient_element["name"],
                "shelf": ingredient_element["shelf"],
                "quantity": quantity,
                "unite": ingredient_element["unite"],
                "price": quantity * ingredient_element["price"],
            }
            logger.debug(
                f"Ingredient informations : {shopping_element['name']} - {shopping_element['shelf']} - {shopping_element['quantity']} - {shopping_element['unite']} - {shopping_element['price']}"
            )
            if shopping_element["name"] in [
                ingredient_element["name"]
                for ingredient_element in shopping_list
            ]:
                # Get ingredient
                ingredient_index = [
                    index
                    for index, ingredient_element in enumerate(shopping_list)
                    if ingredient_element["name"] == shopping_element["name"]
                ][0]
                shopping_list[ingredient_index][
                    "quantity"
                ] += shopping_element["quantity"]
                shopping_list[ingredient_index]["price"] += shopping_element[
                    "price"
                ]
                logger.debug(
                    f"Ingredient already in the shopping list : updating its quantity to {shopping_list[ingredient_index]['quantity']} and its price to {shopping_list[ingredient_index]['price']}"
                )
            else:
                shopping_list.append(shopping_element)
    logger.debug(
        f"Total of {len(shopping_list)} ingredients added to shopping list"
    )
    print_shopping_list(shopping_list)

    # Save shopping list result in a excel spreadsheet
    excel_factory = create_excel_table(
        "shopping_list.xlsx", SHOPPING_LIST_TYPE, log
    )
    for index, shopping_element in enumerate(shopping_list):
        excel_factory.add_ingredient(
            list(shopping_element.values()), 4 + index
        )

    return shopping_list


def _add_ingredient(name: str, shelf: str, price: float, unite: str):
    ingredient = Ingredient(name, shelf, price, unite)
    logger.debug(f"cli:_add_ingredient : {ingredient}")

    if ingredient.check_presence():
        ingredient.update(INGREDIENTS_DATABASE_FILENAME)
    # TODO Why no else here ? -> it's update OR adding, not both I think ???
    # Write ingredients information in json database file
    ingredient.add_to_json_file(INGREDIENTS_DATABASE_FILENAME)


def _add_ingredients(excel_filename: str):
    # Open excel file
    excel_factory = ExcelFactory(click.format_filename(excel_filename))

    # Iter on rows
    for ingredient in excel_factory.iterate_ingredient():
        ingredient.add_or_update(INGREDIENTS_DATABASE_FILENAME)


def _add_recipe(excel_filename: str):
    # Open Excel File
    excel_factory = ExcelFactory(click.format_filename(excel_filename))

    recipe = Recipe(
        excel_factory.get_recipe_name(),
        [r_e for r_e in excel_factory.iterate_recipe_element()],
    )
    recipe.add_to_json_file(RECIPE_DATABASE_FILENAME)


def create_excel_table(name: str, table_type: str, log: bool):
    logger.set_log_activation(log)

    excel_factory = ExcelFactory(name)

    excel_factory.add_title()

    categories = []
    if table_type == INGREDIENT_TYPE:
        categories = INGREDIENTS_CATEGORIES
    elif table_type == RECIPE_TYPE:
        categories = RECIPES_CATEGORIES
    elif table_type == SHOPPING_LIST_TYPE:
        categories = SHOPPING_LIST_CATEGORIES

    excel_factory.create_header_row(categories)

    excel_factory.workbook.save(filename=name)

    return excel_factory
