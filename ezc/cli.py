from typing import List

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
from ezc.json_utility import get_json_ingredient, get_json_recipe
from ezc.recipes import (
    Ingredient,
    Recipe,
    RecipeElement,
    ShoppingElement,
    ShoppingList,
)


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


def _create_list(recipes: List[str], log: bool) -> ShoppingList:
    """Create a shopping list based on recipes list

    Args:
        recipes (List[str]): Recipes list to follow to create shopping list

    Returns:
        _type_: _description_
    """
    shopping_list = ShoppingList([])
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
        recipe = Recipe(
            recipe_name,
            [
                RecipeElement(r_e["ingredient_name"], r_e["quantity"])
                for r_e in recipe_element["ingredients_list"]
            ],
        )

        for ingredient in recipe.ingredients:

            logger.debug(
                f"Adding {ingredient.quantity} {ingredient.ingredient_name} ingredient"
            )
            try:
                ingredient_element = get_json_ingredient(
                    ingredient.ingredient_name
                )
            except IngredientNotFoundException:
                logger.error(
                    f"Ingredient {ingredient.ingredient_name} is not in the ingredients database"
                )
                continue

            ingredient_object = Ingredient(
                ingredient_element["name"],
                ingredient_element["shelf"],
                ingredient_element["price"],
                ingredient_element["unite"],
            )

            shopping_element = ShoppingElement(ingredient_object, ingredient)
            shopping_list.add_or_update_element(shopping_element)

    logger.debug(
        f"Total of {shopping_list.length()} ingredients added to shopping list"
    )
    logger.debug(f"{shopping_list}")
    # print_shopping_list(shopping_list)

    # Save shopping list result in a excel spreadsheet
    excel_factory = create_excel_table(
        "shopping_list.xlsx", SHOPPING_LIST_TYPE, log
    )

    excel_factory.add_shopping_list(shopping_list)

    return shopping_list


def _add_ingredient(name: str, shelf: str, price: float, unite: str):
    ingredient = Ingredient(name, shelf, price, unite)
    logger.debug(f"cli:_add_ingredient : {ingredient}")

    ingredient.add_or_update(INGREDIENTS_DATABASE_FILENAME)


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
