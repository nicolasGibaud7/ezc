import json
import unittest
from configparser import ConfigParser
from typing import Any

from click.testing import CliRunner

from ezc.cli import add_ingredient

CONFIG_FILE = "tests/functional_tests/functional_tests_config.ini"
LOG_STATE = "True"


class AddingIngredient(unittest.TestCase):
    def setUp(self) -> None:
        self.configuration = ConfigParser()
        self.configuration.read(CONFIG_FILE)
        self.original_database_content = (
            self.get_ingredients_database_content()
        )
        self.runner = CliRunner()

    def tearDown(self) -> None:
        self.backup_ingredients_database(self.original_database_content)

    def get_ingredients_database_content(self) -> str:
        database_content = ""
        with open(
            self.configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "r"
        ) as database_file:
            database_content = json.load(database_file)
        return database_content

    def backup_ingredients_database(self, database_content: str) -> None:
        with open(
            self.configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "w"
        ) as database_file:
            json.dump(database_content, database_file, indent=4)

    def compare_database_content(self, compared_content: Any) -> bool:
        with open(
            self.configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "r"
        ) as database_file:
            database_content = json.load(database_file)
        return database_content == compared_content

    def print_database_content(self):
        with open(
            self.configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "r"
        ) as database_file:
            print(json.load(database_file))

    def test_can_add_an_ingredient_and_find_it_later_in_the_database(self):
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
            self.compare_database_content([]),
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
            ),
            f"\n - Output : \n\n{result.output}",
        )


if __name__ == "__main__":
    unittest.main()
