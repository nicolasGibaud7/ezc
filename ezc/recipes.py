from dataclasses import dataclass
from typing import Any, Dict, List

from ezc.json_utility import (
    add_ingredient_to_json_file,
    add_recipe_to_json_file,
    check_ingredient_presence,
    update_ingredient_in_json_file,
)
from ezc.utility import format_option


@dataclass
class Ingredient:
    """
    Represent an ingredient with name, shelf, price, unite info.
    And provide tools to interact with json database to add or update
    an ingredient for example.
    """

    name: str
    shelf: str
    price: float
    unite: str = "kg"

    def to_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "shelf": self.shelf,
            "price": self.price,
            "unite": self.unite,
        }

    def check_presence(self, database: str) -> bool:
        return check_ingredient_presence(self.name, database)

    def update(self, database: str):
        update_ingredient_in_json_file(database, self.to_json())

    def add_to_json_file(self, database: str):
        add_ingredient_to_json_file(database, self.to_json())

    def add_or_update(self, database: str):
        """Add an ingredient to a json database if it's not in it, else
        update ingredient info.

        Args:
            database (str): json database name
        """
        if self.check_presence(database):
            self.update(database)
        else:
            self.add_to_json_file(database)

    def __post_init__(self):
        self.name = format_option(self.name)
        self.shelf = format_option(self.shelf)
        self.price = format_option(self.price)
        self.unite = format_option(self.unite)


@dataclass
class RecipeElement:
    """
    Represent an element of a recipe.
    """

    ingredient_name: str
    quantity: float

    def to_json(self) -> Dict[str, Any]:
        return {
            "ingredient_name": self.ingredient_name,
            "quantity": self.quantity,
        }

    def __post_init__(self):
        self.ingredient_name = format_option(self.ingredient_name)
        self.quantity = format_option(self.quantity)


@dataclass
class Recipe:
    """
    Recipe object which contains a group of recipe elements and provide tool to
    add the recipe to a json database.
    """

    name: str
    recipe_elements: List[
        RecipeElement
    ]  # TODO change ingredients attribute name to recipe_elements

    def to_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "ingredients_list": [
                ingredient.to_json() for ingredient in self.recipe_elements
            ],
        }

    def add_to_json_file(self, database: str):
        add_recipe_to_json_file(
            database, self.name, self.to_json()["ingredients_list"]
        )

    def __post_init__(self):
        self.name = format_option(self.name)
