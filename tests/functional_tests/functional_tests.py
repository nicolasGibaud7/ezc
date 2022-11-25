import json
import unittest
from configparser import ConfigParser
from typing import Any

from click.testing import CliRunner

from ezc.cli import add_ingredient, add_recipe

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

    def test_can_add_an_ingredient_and_find_it_in_the_database(self):
        # Joe heard that there is a cool new app which permit to add store
        # ingredients to build recipes with them

        # Joe wants to add a first courgette ingredient but forget to add ingredient name
        result = self.runner.invoke(
            add_ingredient,
            [
                "--shelf",
                "LEGUMES",
                "--price",
                "0.8",
                "--category",
                "market",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
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
            [
                "--name",
                "courgette",
                "--shelf",
                "LEGUMES",
                "--price",
                "0.8",
                "--category",
                "market",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": float("0.8"),
                        "category": "market",
                        "unite": "kg",
                    }
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Joe wan't now to add another ingredient to the database but enter a no existing category
        result = self.runner.invoke(
            add_ingredient,
            [
                "--name",
                "carotte",
                "--shelf",
                "LEGUMES",
                "--price",
                "1.21",
                "--category",
                "mrket",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 2, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": float("0.8"),
                        "category": "market",
                        "unite": "kg",
                    }
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Joe retry more carefully to a add a new ingredient to the database
        result = self.runner.invoke(
            add_ingredient,
            [
                "--name",
                "carotte",
                "--shelf",
                "LEGUMES",
                "--price",
                "1.21",
                "--category",
                "market",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": 0.8,
                        "category": "market",
                        "unite": "kg",
                    },
                    {
                        "name": "carotte",
                        "shelf": "legumes",
                        "price": 1.21,
                        "category": "market",
                        "unite": "kg",
                    },
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Joe see that carrot price drop down and wan't to modify
        # the carrot item in ingredient database
        result = self.runner.invoke(
            add_ingredient,
            [
                "--name",
                "carotte",
                "--shelf",
                "LEGUMES",
                "--price",
                "0.99",
                "--category",
                "market",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": 0.8,
                        "category": "market",
                        "unite": "kg",
                    },
                    {
                        "name": "carotte",
                        "shelf": "legumes",
                        "price": 0.99,
                        "category": "market",
                        "unite": "kg",
                    },
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

    def test_add_ingredient_for_building_a_recipe(self):
        # Martin want's to create risotto recipe
        # He begins by adding rice ingredient
        result = self.runner.invoke(
            add_ingredient,
            [
                "--name",
                "round rice",
                "--shelf",
                "EPICERIE_SALEE",
                "--price",
                "1",
                "--category",
                "supermarket",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "round rice",
                        "shelf": "epicerie_salee",
                        "price": 1,
                        "category": "supermarket",
                        "unite": "kg",
                    },
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output} \n - Database : {self.print_database_content()}",
        )

        # Martin continue by adding courgette ingredient
        result = self.runner.invoke(
            add_ingredient,
            [
                "--name",
                "courgette",
                "--shelf",
                "LEGUMES",
                "--price",
                "0.8",
                "--category",
                "market",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "round rice",
                        "shelf": "epicerie_salee",
                        "price": 1,
                        "category": "supermarket",
                        "unite": "kg",
                    },
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": 0.8,
                        "category": "market",
                        "unite": "kg",
                    },
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # Martin follow by adding onions to the database

        result = self.runner.invoke(
            add_ingredient,
            [
                "--name",
                "onion",
                "--shelf",
                "LEGUMES",
                "--price",
                "0.95",
                "--category",
                "market",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "round rice",
                        "shelf": "epicerie_salee",
                        "price": 1,
                        "category": "supermarket",
                        "unite": "kg",
                    },
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": 0.8,
                        "category": "market",
                        "unite": "kg",
                    },
                    {
                        "name": "onion",
                        "shelf": "legumes",
                        "price": 0.95,
                        "category": "market",
                        "unite": "kg",
                    },
                ],
                "INGREDIENTS_DATABASE",
            ),
            f"\n - Output : \n\n{result.output}",
        )

        # And Martin finish adding ingredient by putting parmesan ingredient in the database
        result = self.runner.invoke(
            add_ingredient,
            [
                "--name",
                "parmesan",
                "--shelf",
                "FRAIS",
                "--price",
                "10.28",
                "--category",
                "supermarket",
                "--unite",
                "kg",
                "--config",
                CONFIG_FILE,
                "--log",
                LOG_STATE,
            ],
        )
        self.assertEqual(
            result.exit_code, 0, f"\n - Output : \n\n{result.output}"
        )
        self.assertTrue(
            self.compare_database_content(
                [
                    {
                        "name": "round rice",
                        "shelf": "epicerie_salee",
                        "price": 1,
                        "category": "supermarket",
                        "unite": "kg",
                    },
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": 0.8,
                        "category": "market",
                        "unite": "kg",
                    },
                    {
                        "name": "onion",
                        "shelf": "legumes",
                        "price": 0.95,
                        "category": "market",
                        "unite": "kg",
                    },
                    {
                        "name": "parmesan",
                        "shelf": "frais",
                        "price": 10.28,
                        "category": "supermarket",
                        "unite": "kg",
                    },
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
                [
                    {
                        "name": "risotto_recipe",
                        "ingredients_list": [
                            {"ingredient_name": "round rice", "quantity": 1},
                            {"ingredient_name": "courgette", "quantity": 1.5},
                            {"ingredient_name": "onion", "quantity": 2},
                            {"ingredient_name": "parmesan", "quantity": 0.1},
                        ],
                    }
                ],
                "RECIPES_DATABASE",
            )
        )


if __name__ == "__main__":
    unittest.main()
