import glob
import json
import os
import unittest
from configparser import ConfigParser
from typing import Any

from click.testing import CliRunner
from data.data_add_ingredient_for_building_a_recipe import (
    courgette,
    courgette_representation,
    onion,
    onion_representation,
    parmesan,
    parmesan_representation,
    risotto_representation,
    round_rice,
    round_rice_representation,
)
from data.data_add_recipe_by_created_excel_file import (
    recipe_categories,
    recipe_columns_names,
    recipe_ingredients,
)
from data.data_adding_ingredients import (
    carrot,
    carrot_bad_category,
    carrot_representation,
    courgette_missing_name_param,
    lower_price_carrot,
    lower_price_carrot_representation,
)
from data.data_create_shopping_list import (
    FROZEN_FOOD_SHOPPING_LIST_FILENAME,
    MARKET_SHOPPING_LIST_FILENAME,
    SUPERMARKET_SHOPPING_LIST_FILENAME,
    get_associate_expected_result,
)
from openpyxl.styles import Alignment, Border, Font, Side

from ezc.cli import (
    add_ingredient,
    add_ingredients,
    add_recipe,
    create_list,
    create_table,
)
from ezc.constants import (
    EXCEL_COLUMNS,
    INGREDIENT_TYPE,
    RECIPE_TYPE,
    TITLE_CELL,
)
from ezc.excel_factory import ExcelFactory
from tests.functional_tests.data.data_adding_multiple_ingredients_by_created_excel_files import (
    ingredient_columns_names,
    ingredients_categories,
    new_ingredients,
)

CONFIG_FILE = "tests/functional_tests/functional_tests_config.ini"
ADDING_RECIPE_BY_EXCEL_TABLE_CONFIG_FILE = (
    "tests/functional_tests/adding_recipe_by_excel_table_config.ini"
)
CREATE_SHOPPING_LIST_CONFIG = (
    "tests/functional_tests/create_shopping_list_config.ini"
)
LOG_STATE = "True"


class NewUser(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()
        self.configuration = ConfigParser()
        self.configuration.read(CONFIG_FILE)
        self.original_ingredient_database_content = self.get_database_content(
            "INGREDIENTS_DATABASE"
        )
        self.original_recipe_database_content = self.get_database_content(
            "RECIPES_DATABASE"
        )

    def tearDown(self) -> None:
        self.backup_database("INGREDIENTS_DATABASE")
        self.backup_database("RECIPES_DATABASE")
        try:
            os.remove("new_ingredients.xlsx")
        except FileNotFoundError:  # It's for tests which didn't create new_ingredients.xlsx file
            pass
        try:
            os.remove(MARKET_SHOPPING_LIST_FILENAME)
            os.remove(SUPERMARKET_SHOPPING_LIST_FILENAME)
            os.remove(FROZEN_FOOD_SHOPPING_LIST_FILENAME)

        except FileNotFoundError:  # It's for tests which didn't create new_ingredients.xlsx file
            pass

    def get_database_content(self, database_name: str) -> Any:
        with open(
            self.configuration.get("CONFIG", database_name), "r"
        ) as database_file:
            return json.load(database_file)

    def backup_database(self, database_name: str):
        if "INGREDIENTS" in database_name:
            content = self.original_ingredient_database_content
        elif "RECIPES" in database_name:
            content = self.original_recipe_database_content
        else:
            content = ""

        with open(
            self.configuration.get("CONFIG", database_name), "w"
        ) as database_file:
            json.dump(content, database_file, indent=4)

    def print_database_content(self):
        with open(
            self.configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "r"
        ) as database_file:
            print(json.load(database_file))

    def test_adding_ingredients(self):
        # Joe heard that there is a cool new app which permit to add store
        # ingredients to build recipes with them

        # Joe wants to add a first courgette ingredient but forget to add ingredient name
        result = self.runner.invoke(
            add_ingredient,
            courgette_missing_name_param(CONFIG_FILE, LOG_STATE),
        )
        self.assertEqual(
            result.exit_code, 2, f"\n - Output : \n\n{result.output}"
        )
        self.assertEqual([], self.get_database_content("INGREDIENTS_DATABASE"))

        # Joe learn from his mistake and run valid add_ingredient command
        # to add his first ingredient to the database
        result = self.runner.invoke(
            add_ingredient,
            courgette(CONFIG_FILE, LOG_STATE),
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

        # Joe wan't now to add another ingredient to the database but enter a no existing category
        result = self.runner.invoke(
            add_ingredient, carrot_bad_category(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 2, f"\n - Output : \n\n{result.output}"
        )
        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

        # Joe retry more carefully to a add a new ingredient to the database
        result = self.runner.invoke(
            add_ingredient, carrot(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )

        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            carrot_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

        # Joe see that carrot price drop down and wan't to modify
        # the carrot item in ingredient database
        result = self.runner.invoke(
            add_ingredient, lower_price_carrot(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )

        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            lower_price_carrot_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

    def test_add_ingredient_for_building_a_recipe(self):
        # Martin want's to create risotto recipe
        # He begins by adding rice ingredient
        result = self.runner.invoke(
            add_ingredient, round_rice(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )

        self.assertIn(
            round_rice_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

        # Martin continue by adding courgette ingredient
        result = self.runner.invoke(
            add_ingredient, courgette(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )

        self.assertIn(
            round_rice_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

        # Martin follow by adding onions to the database

        result = self.runner.invoke(
            add_ingredient, onion(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertIn(
            round_rice_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            onion_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

        # And Martin finish adding ingredient by putting parmesan ingredient in the database
        result = self.runner.invoke(
            add_ingredient, parmesan(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )

        self.assertIn(
            round_rice_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            onion_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            parmesan_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

        # Martin could finally create risotto recipe based on all added ingredients
        result = self.runner.invoke(
            add_recipe,
            [
                "tests/functional_tests/excel_files/risotto_recipe.xlsx",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            risotto_representation(),
            self.get_database_content("RECIPES_DATABASE"),
        )

    def test_adding_multiple_ingredients_by_created_excel_files(self):
        # Esteban is a lazy smart guy and wan't to add several ingredients to the database
        # So he wan't to use excel tables to do it

        # Esteban begins by generating dedicated "ingredients table"
        self.runner.invoke(
            create_table,
            [
                "--name",
                "new_ingredients.xlsx",
                "--table_type",
                INGREDIENT_TYPE,
                "--log",
                LOG_STATE,
            ],
        )
        excel_file = ExcelFactory("new_ingredients.xlsx")
        self.assertEqual(
            excel_file.current_sheet[TITLE_CELL].font,
            Font(bold=True),
        )
        self.assertEqual(
            excel_file.current_sheet[TITLE_CELL].border,
            Border(
                bottom=Side(border_style="thin"),
                top=Side(border_style="thin"),
                left=Side(border_style="thin"),
                right=Side(border_style="thin"),
            ),
        )
        self.assertEqual(
            excel_file.current_sheet[TITLE_CELL].alignment,
            Alignment(horizontal="center", vertical="center"),
        )
        self.assertEqual(
            excel_file.current_sheet[TITLE_CELL].value, "New_ingredients"
        )
        for index, header_column in enumerate(EXCEL_COLUMNS[0:5]):
            cell = excel_file.current_sheet[f"{header_column}3"]
            self.assertEqual(cell.value, ingredients_categories[index])
            self.assertEqual(cell.style, "Headline 2")

        # Next, Esteban will manually add some ingredients to the "ingredients table"
        for index, new_ingredient in enumerate(new_ingredients):
            for col, col_name in ingredient_columns_names:
                excel_file.current_sheet[
                    f"{col}{4+index}"
                ].value = new_ingredient[col_name]

        excel_file.workbook.save(excel_file.name)

        # Finally, Esteban will add all "ingredients table" ingredients to the database
        self.runner.invoke(
            add_ingredients,
            [
                "new_ingredients.xlsx",
                "--config",
                CONFIG_FILE,
                "--log" if LOG_STATE else "--no-log",
            ],
        )
        self.assertIn(
            courgette_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            round_rice_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            onion_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )
        self.assertIn(
            parmesan_representation(),
            self.get_database_content("INGREDIENTS_DATABASE"),
        )

    def test_add_recipe_by_created_excel_file(self):

        # John wan't to add a new recipe and don't get an excel file with all ingredients
        # So he must create it and add all recipe ingredients to add the recipe

        # John generates dedicated adding recipe excel table
        self.runner.invoke(
            create_table,
            [
                "--name",
                "risotto.xlsx",
                "--table_type",
                RECIPE_TYPE,
                "--log",
                LOG_STATE,
            ],
        )
        excel_file = ExcelFactory("risotto.xlsx")
        self.assertEqual(
            excel_file.current_sheet[TITLE_CELL].font,
            Font(bold=True),
        )
        self.assertEqual(
            excel_file.current_sheet[TITLE_CELL].border,
            Border(
                bottom=Side(border_style="thin"),
                top=Side(border_style="thin"),
                left=Side(border_style="thin"),
                right=Side(border_style="thin"),
            ),
        )
        self.assertEqual(
            excel_file.current_sheet[TITLE_CELL].alignment,
            Alignment(horizontal="center", vertical="center"),
        )
        self.assertEqual(excel_file.current_sheet[TITLE_CELL].value, "Risotto")
        for index, header_column in enumerate(EXCEL_COLUMNS[0:2]):
            cell = excel_file.current_sheet[f"{header_column}3"]
            self.assertEqual(cell.value, recipe_categories[index])
            self.assertEqual(cell.style, "Headline 2")

        # John manually add recipe ingredients to the excel table
        for index, recipe_ingredient in enumerate(recipe_ingredients):
            for i, col in enumerate(recipe_columns_names):
                excel_file.current_sheet[
                    f"{col}{4+index}"
                ].value = recipe_ingredient[i]

        excel_file.workbook.save(excel_file.name)

        # John try to add the recipe to the database but one ingredient is missing
        result = self.runner.invoke(
            add_recipe,
            [
                "risotto.xlsx",
                "--config",
                ADDING_RECIPE_BY_EXCEL_TABLE_CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )

        self.assertEqual(
            result.exit_code, 0
        )  # TODO Add the end of the scenario when recipe ingredients will be verified

        self.assertIn(
            risotto_representation(),
            self.get_database_content("RECIPES_DATABASE"),
        )

        # John add missing ingredient to the database

        # John try again to add the recipe to the database and success !

    def test_create_shopping_list(self):

        # Anna want's to to create shopping list for the week
        # She planned to make 2 recipes for this week
        # She already registered recipes and associated ingredients in the database
        configuration = ConfigParser()
        configuration.read(CREATE_SHOPPING_LIST_CONFIG)

        # Anna creates shopping list by telling on what recipes it will be built
        result = self.runner.invoke(
            create_list,
            [
                "risotto",
                "pesto pasta",
                "--config",
                CREATE_SHOPPING_LIST_CONFIG,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Check that all shopping lists are really created
        shopping_lists = glob.glob("*_list.xlsx")
        self.assertIn(FROZEN_FOOD_SHOPPING_LIST_FILENAME, shopping_lists)
        self.assertIn(SUPERMARKET_SHOPPING_LIST_FILENAME, shopping_lists)
        self.assertIn(MARKET_SHOPPING_LIST_FILENAME, shopping_lists)

        # Check shopping lists content
        for shopping_list in shopping_lists:
            excel = ExcelFactory(shopping_list)

            for exp_elem in get_associate_expected_result(shopping_list):
                self.assertEqual(
                    excel.current_sheet[exp_elem[0]].value, exp_elem[1]
                )


if __name__ == "__main__":
    unittest.main()
