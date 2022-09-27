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

    def check_presence(self) -> bool:
        return check_ingredient_presence(self.name)

    def update(self, database: str):
        update_ingredient_in_json_file(database, self.to_json())

    def add_to_json_file(self, database: str):
        add_ingredient_to_json_file(database, self.to_json())

    def add_or_update(self, database: str):
        if self.check_presence():
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
    name: str
    ingredients: List[RecipeElement]

    def to_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "ingredients_list": [
                ingredient.to_json() for ingredient in self.ingredients
            ],
        }

    def add_to_json_file(self, database: str):
        add_recipe_to_json_file(
            database, self.name, [r_e.to_json() for r_e in self.ingredients]
        )

    def __post_init__(self):
        self.name = format_option(self.name)
