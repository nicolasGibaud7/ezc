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
from ezc.utility import format_option, print_shopping_list


@click.group()
def cli():
    pass


@cli.command()
@click.argument("recipes", nargs=-1)
@click.option("-l", "--log", type=bool, required=False, default=False)
def create_list(recipes: List[str], log: bool):
    logger.set_log_activation(log)
    shopping_list = []
    logger.debug(
        f"Creating shopping list for {len(recipes)} recipes : {' - '.join(recipes)}"
    )
    for recipe_name in recipes:
        logger.debug(f"Adding {recipe_name} recipe ingredients")
        try:
            recipe_element = get_json_recipe(recipe_name)
        except Exception:  # TODO Use RecipeNotFoundException instead
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
            except Exception:  # TODO Use IngredientNotFoundException instead
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

    logger.debug(
        f"Adding ingredient {name} from {shelf} shelf at the price of {price}/{unite}."
    )

    if check_ingredient_presence(name):
        update_ingredient_in_json_file(
            INGREDIENTS_DATABASE_FILENAME, name, shelf, price, unite
        )

    # Write ingredients information in json database file
    add_ingredient_to_json_file(
        INGREDIENTS_DATABASE_FILENAME, name, shelf, price, unite
    )


@cli.command()
@click.argument("excel_filename", type=click.Path(exists=True))
@click.option("--log / --no-log", required=False, default=False)
def add_ingredients(excel_filename: str, log: bool):
    logger.set_log_activation(log)

    # Open excel file
    excel_factory = ExcelFactory(click.format_filename(excel_filename))
    new_ingredients_list = []
    updated_ingredients_list = []
    # Iter on rows
    for ingredient in excel_factory.iterate_ingredients():
        # TODO Check if ingredient is existing and update it if it exists
        ingredient = list(
            map(
                format_option,
                [element.value for element in ingredient],
            )
        )
        if check_ingredient_presence(ingredient[0]):
            updated_ingredients_list.append(ingredient)
        else:
            new_ingredients_list.append(ingredient)

    logger.debug(f"New ingredients list : {new_ingredients_list}")
    logger.debug(f"Updated ingredients list : {updated_ingredients_list}")
    update_ingredients_in_json_file(
        INGREDIENTS_DATABASE_FILENAME, updated_ingredients_list
    )
    add_ingredients_to_json_file(
        INGREDIENTS_DATABASE_FILENAME, new_ingredients_list
    )


@cli.command()
@click.argument("excel_filename", type=click.Path(exists=True))
@click.option("-l", "--log", type=bool, required=False, default=False)
def add_recipe(excel_filename: str, log: bool):
    logger.set_log_activation(log)

    # Open Excel File
    excel_factory = ExcelFactory(click.format_filename(excel_filename))
    ingredients_list = []
    recipe_name = excel_factory.get_recipe_name()

    for ingredient in excel_factory.iterate_ingredients():
        ingredient_name, ingredient_quantity = map(
            format_option, [element.value for element in ingredient]
        )
        ingredients_list.append(
            {
                "ingredient_name": ingredient_name,
                "quantity": ingredient_quantity,
            }
        )

    # Add recipe to database
    add_recipe_to_json_file(
        RECIPE_DATABASE_FILENAME, recipe_name, ingredients_list
    )


@cli.command()
@click.option("-n", "--name", type=str, default="table.xlsx")
@click.option("-t", "--table_type", type=click.Choice(TABLE_TYPE_LIST))
@click.option("-l", "--log", type=bool, required=False, default=False)
def create_table(name: str, table_type: str, log: bool):
    create_excel_table(name, table_type, log)


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
