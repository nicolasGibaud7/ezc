from configparser import ConfigParser
from typing import List

import click

from ezc.constants import (
    CATEGORIES,
    INGREDIENT_TYPE,
    INGREDIENTS_CATEGORIES,
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
from ezc.recipes import Ingredient, Recipe, RecipeElement
from ezc.shopping import ShoppingElement, ShoppingList


@click.group()
def cli():
    pass


@cli.command()
@click.argument("recipes", nargs=-1)
@click.option(
    "--config", type=str, required=False, default="default_config.json"
)
@click.option("-l", "--log", type=bool, required=False, default=False)
def create_list(recipes: List[str], config: str, log: bool):
    logger.set_log_activation(log)
    configuration = ConfigParser()
    configuration.read(config)
    _create_list(recipes, configuration, log)


@cli.command()
@click.option("-n", "--name", type=str, required=True)
@click.option("-s", "--shelf", type=click.Choice(SHELF_LIST), required=True)
@click.option("-p", "--price", type=float, required=True)
@click.option("-c", "--category", type=click.Choice(CATEGORIES), required=True)
@click.option("-u", "--unite", type=str, required=False, default="kg")
@click.option(
    "--config", type=str, required=False, default="default_config.json"
)
@click.option("-l", "--log", type=bool, required=False, default=False)
def add_ingredient(
    name: str,
    shelf: str,
    price: float,
    category: str,
    unite: str,
    config: str,
    log: bool,
):
    """Add an individual ingredient to the json database by passing all ingredient info

    Args:
        name (str): Ingredient name
        shelf (str): Ingredient shelf
        price (float): Ingredient price
        category(str): Ingredient category
        unite (str): Ingredient unite
        log (bool): Is log activated or not
    """
    configuration = ConfigParser()
    configuration.read(config)
    logger.set_log_activation(log)
    _add_ingredient(name, shelf, price, category, unite, configuration)


@cli.command()
@click.argument("excel_filename", type=click.Path(exists=True))
@click.option(
    "--config", type=str, required=False, default="default_config.json"
)
@click.option("--log / --no-log", required=False, default=False)
def add_ingredients(excel_filename: str, config: str, log: bool):
    """Add a group of ingredients described in a dedicated excel file
    to json ingredient database

    Args:
        excel_filename (str): Ingredients description
        log (bool): Is log activated or not
    """
    logger.set_log_activation(log)
    configuration = ConfigParser()
    configuration.read(config)
    _add_ingredients(excel_filename, configuration)


@cli.command()
@click.argument("excel_filename", type=click.Path(exists=True))
@click.option(
    "--config", type=str, required=False, default="default_config.json"
)
@click.option("-l", "--log", type=bool, required=False, default=False)
def add_recipe(excel_filename: str, config: str, log: bool):
    """Add a recipe to json recipe database based on a recipe description
    in an excel file

    Args:
        excel_filename (str): Recipe description
        log (bool): Is log activated or not
    """
    logger.set_log_activation(log)
    configuration = ConfigParser()
    configuration.read(config)
    _add_recipe(excel_filename, configuration)


@cli.command()
@click.option("-n", "--name", type=str, default="table.xlsx")
@click.option("-t", "--table_type", type=click.Choice(TABLE_TYPE_LIST))
@click.option("-l", "--log", type=bool, required=False, default=False)
def create_table(name: str, table_type: str, log: bool):
    create_excel_table(name, table_type, log)


def _create_list(
    recipes: List[str], configuration: ConfigParser, log: bool
) -> ShoppingList:
    """Create a shopping list based on recipes list

    Args:
        recipes (List[str]): Recipes list to follow to create shopping list

    Returns:
        ShoppingList: Shopping list representation
    """
    shopping_list = ShoppingList([])
    logger.debug(
        f"Creating shopping list for {len(recipes)} recipes : {' - '.join(recipes)}"
    )
    for recipe_name in recipes:
        logger.debug(f"Adding {recipe_name} recipe ingredients")
        try:
            recipe_element = get_json_recipe(
                recipe_name,
                configuration.get("CONFIG", "RECIPES_DATABASE"),
            )
        except RecipeNotFoundException:
            logger.error(
                f"Recipe {recipe_name} is not in the recipes database. Please add it."
            )
            continue
        recipe = Recipe(
            recipe_name,
            [
                RecipeElement(r_e["ingredient_name"], r_e["quantity"])
                for r_e in recipe_ingredient["ingredients_list"]
            ],
        )

        for recipe_element in recipe.recipe_elements:

            logger.debug(
                f"Adding {recipe_element.quantity} {recipe_element.ingredient_name} ingredient"
            )
            try:
                ingredient_element = get_json_ingredient(
                    recipe_element.ingredient_name,
                    configuration.get("CONFIG", "INGREDIENTS_DATABASE"),
                )
            except IngredientNotFoundException:
                logger.error(
                    f"{recipe_element.ingredient_name} not in ingredient database"
                )
                continue

            ingredient = Ingredient(
                ingredient_element["name"],
                ingredient_element["shelf"],
                ingredient_element["price"],
                ingredient_element["category"],
                ingredient_element["unite"],
            )

            shopping_element = ShoppingElement(
                ingredient, recipe_element.quantity
            )
            shopping_list.add_or_update_element(shopping_element)

    logger.debug(
        f"Total of {shopping_list.length()} ingredients added to shopping list"
    )
    logger.debug(f"{shopping_list}")
    # print_shopping_list(shopping_list)

    # Save shopping list result in a excel spreadsheet
    for category in CATEGORIES:
        excel_factory = create_excel_table(
            f"{category}_list.xlsx", SHOPPING_LIST_TYPE, log
        )
        excel_factory.add_shopping_list(
            shopping_list.__getattribute__(
                category
            )  # Access to category attribute
        )

    return shopping_list


def _add_ingredient(
    name: str,
    shelf: str,
    price: float,
    category: str,
    unite: str,
    configuration: ConfigParser,
):
    ingredient = Ingredient(name, shelf, price, category, unite)
    logger.debug(f"cli:_add_ingredient : {ingredient}")

    ingredient.add_or_update(
        configuration.get("CONFIG", "INGREDIENTS_DATABASE")
    )


def _add_ingredients(excel_filename: str, configuration: ConfigParser):
    # Open excel file
    excel_factory = ExcelFactory(click.format_filename(excel_filename))

    # Iter on rows
    for ingredient in excel_factory.iterate_ingredient():
        ingredient.add_or_update(
            configuration.get("CONFIG", "INGREDIENTS_DATABASE")
        )


def _add_recipe(excel_filename: str, configuration: ConfigParser):
    # Open Excel File
    excel_factory = ExcelFactory(click.format_filename(excel_filename))

    recipe = Recipe(
        excel_factory.get_recipe_name(),
        [r_e for r_e in excel_factory.iterate_recipe_element()],
    )
    recipe.add_to_json_file(configuration.get("CONFIG", "RECIPES_DATABASE"))


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
