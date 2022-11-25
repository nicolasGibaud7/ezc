import json
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
from data.data_adding_ingredients import (
    carrot,
    carrot_bad_category,
    carrot_representation,
    courgette_missing_name_param,
    lower_price_carrot,
    lower_price_carrot_representation,
)
from openpyxl.styles import Alignment, Border, Font, Side

from ezc.cli import add_ingredient, add_ingredients, add_recipe, create_table
from ezc.constants import EXCEL_COLUMNS, INGREDIENT_TYPE, TITLE_CELL
from ezc.excel_factory import ExcelFactory
from tests.functional_tests.data.data_adding_multiple_ingredients_by_created_excel_files import (
    columns_names,
    ingredients_categories,
    new_ingredients,
)

CONFIG_FILE = "tests/functional_tests/functional_tests_config.ini"
LOG_STATE = "True"


class NewUser(unittest.TestCase):
    def setUp(self) -> None:
        self.configuration = ConfigParser()
        self.configuration.read(CONFIG_FILE)
        self.original_ingredient_database_content = self.get_database_content(
            "INGREDIENTS_DATABASE"
        )
        self.original_recipe_database_content = self.get_database_content(
            "RECIPES_DATABASE"
        )
        self.runner = CliRunner()

    def tearDown(self) -> None:
        self.backup_database("INGREDIENTS_DATABASE")
        self.backup_database("RECIPES_DATABASE")

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

    def compare_database_content(
        self,
        compared_content: Any,
        database_name: str,
    ) -> bool:
        with open(
            self.configuration.get("CONFIG", database_name), "r"
        ) as database_file:
            return json.load(database_file) == compared_content

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
        self.assertTrue(
            self.compare_database_content([], "INGREDIENTS_DATABASE"),
            f"\n - Output : \n\n{result.output}",
        )

        # Joe learn from his mistake and run valid add_ingredient command
        # to add his first ingredient to the database
        result = self.runner.invoke(
            add_ingredient,
            courgette(CONFIG_FILE, LOG_STATE),
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [courgette_representation()],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Joe wan't now to add another ingredient to the database but enter a no existing category
        result = self.runner.invoke(
            add_ingredient, carrot_bad_category(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 2, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [courgette_representation()],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Joe retry more carefully to a add a new ingredient to the database
        result = self.runner.invoke(
            add_ingredient, carrot(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [courgette_representation(), carrot_representation()],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Joe see that carrot price drop down and wan't to modify
        # the carrot item in ingredient database
        result = self.runner.invoke(
            add_ingredient, lower_price_carrot(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    courgette_representation(),
                    lower_price_carrot_representation(),
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
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
        self.assertTrue(
            self.compare_database_content(
                [round_rice_representation()],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output} \n - Database : {self.print_database_content()}",
        )

        # Martin continue by adding courgette ingredient
        result = self.runner.invoke(
            add_ingredient, courgette(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [round_rice_representation(), courgette_representation()],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Martin follow by adding onions to the database

        result = self.runner.invoke(
            add_ingredient, onion(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    round_rice_representation(),
                    courgette_representation(),
                    onion_representation(),
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # And Martin finish adding ingredient by putting parmesan ingredient in the database
        result = self.runner.invoke(
            add_ingredient, parmesan(CONFIG_FILE, LOG_STATE)
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    round_rice_representation(),
                    courgette_representation(),
                    onion_representation(),
                    parmesan_representation(),
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
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
        self.assertTrue(
            self.compare_database_content(
                risotto_representation(),
                "RECIPES_DATABASE",
            )
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
            for col, col_name in columns_names:
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


if __name__ == "__main__":
    unittest.main()
