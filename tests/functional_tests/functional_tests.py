import json
import unittest
from configparser import ConfigParser
from typing import Any

import pytest
from click.testing import CliRunner

from ezc.cli import add_ingredient
from tests.functional_tests.data.data_functional_tests import (
    data_func_add_ingredient,
)

CONFIG_FILE = "tests/functional_tests/functional_tests_config.ini"
LOG_STATE = "True"


def get_ingredients_database_content(
    configuration: ConfigParser,
) -> str:
    database_content = ""
    with open(
        configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "r"
    ) as database_file:
        database_content = json.load(database_file)
    return database_content


def backup_ingredients_database(
    configuration: ConfigParser, database_content: str
) -> None:
    with open(
        configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "w"
    ) as database_file:
        json.dump(database_content, database_file, indent=4)


def compare_database_content(
    configuration: ConfigParser, compared_content: Any
) -> bool:
    with open(
        configuration.get("CONFIG", "INGREDIENTS_DATABASE"), "r"
    ) as database_file:
        database_content = json.load(database_file)
    return database_content == compared_content


@pytest.mark.parametrize(
    "name, shelf, price, category, unite", data_func_add_ingredient
)
def _add_ingredient(
    name: str,
    shelf: str,
    price: str,
    category: str,
    unite: str,
):
    # Joe wan't to add a single ingredient on database but he's not very good
    configuration = ConfigParser()
    configuration.read(CONFIG_FILE)
    original_database_content = get_ingredients_database_content(configuration)
    # Joe open Terminal
    runner = CliRunner()

    # Joe run add_ingredient command but forgot to add name information so it failed
    result = runner.invoke(
        add_ingredient,
        [
            "--shelf",
            f"{shelf}",
            "--price",
            f"{price}",
            "--category",
            f"{category}",
            "--unite",
            f"{unite}",
            "--config",
            CONFIG_FILE,
            "--log",
            LOG_STATE,
        ],
    )
    assert result.exit_code == 2
    assert compare_database_content(configuration, [])

    # Joe run valid add_ingredient command by learning from his mistake
    result = runner.invoke(
        add_ingredient,
        [
            "--name",
            f"{name}",
            "--shelf",
            f"{shelf}",
            "--price",
            f"{price}",
            "--category",
            f"{category}",
            "--unite",
            f"{unite}",
            "--config",
            CONFIG_FILE,
            "--log",
            LOG_STATE,
        ],
    )
    assert result.exit_code == 0
    assert compare_database_content(
        configuration,
        [
            {
                "name": f"{name}",
                "shelf": f"{shelf}".lower(),
                "price": float(price),
                "category": f"{category}",
                "unite": f"{unite}",
            }
        ],
    )

    # Joe wan't now to add another ingredient to the database but enter a no existing category
    result = runner.invoke(
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
    assert result.exit_code == 2
    assert compare_database_content(
        configuration,
        [
            {
                "name": f"{name}",
                "shelf": f"{shelf}".lower(),
                "price": float(price),
                "category": f"{category}",
                "unite": f"{unite}",
            }
        ],
    )

    # Joe retry more carefully to a add a new ingredient to the database
    result = runner.invoke(
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
    assert result.exit_code == 0
    assert compare_database_content(
        configuration,
        [
            {
                "name": f"{name}",
                "shelf": f"{shelf}".lower(),
                "price": float(price),
                "category": f"{category}",
                "unite": f"{unite}",
            },
            {
                "name": "carotte",
                "shelf": "legumes",
                "price": 1.21,
                "category": "market",
                "unite": "kg",
            },
        ],
    )

    # Joe see that carrot price drop down and wan't to modify
    # the carrot item in ingredient database
    result = runner.invoke(
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
    assert result.exit_code == 0
    assert compare_database_content(
        configuration,
        [
            {
                "name": f"{name}",
                "shelf": f"{shelf}".lower(),
                "price": float(price),
                "category": f"{category}",
                "unite": f"{unite}",
            },
            {
                "name": "carotte",
                "shelf": "legumes",
                "price": 0.99,
                "category": "market",
                "unite": "kg",
            },
        ],
    )

    backup_ingredients_database(configuration, original_database_content)


class AddingIngredient(unittest.TestCase):
    def setUp(self) -> None:
        self.configuration = ConfigParser()
        self.configuration.read(CONFIG_FILE)
        self.original_database_content = get_ingredients_database_content(
            self.configuration
        )
        self.runner = CliRunner()

    def tearDown(self) -> None:
        backup_ingredients_database(
            self.configuration, self.original_database_content
        )

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
        self.assertEqual(result.exit_code, 2)
        self.assertTrue(compare_database_content(self.configuration, []))

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
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(
            compare_database_content(
                self.configuration,
                [
                    {
                        "name": "courgette",
                        "shelf": "legumes",
                        "price": float("0.8"),
                        "category": "market",
                        "unite": "kg",
                    }
                ],
            )
        )

        self.fail("Finish the test !")


if __name__ == "__main__":
    unittest.main()
