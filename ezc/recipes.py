from dataclasses import dataclass, field
from typing import Any, Dict, List

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

    def __post_init__(self):
        self.name = format_option(self.name)
        self.shelf = format_option(self.shelf)
        self.price = format_option(self.price)
        self.unite = format_option(self.unite)


@dataclass
class RecipeElement:
    ingredient: Ingredient
    quantity: int

    def to_json(self) -> Dict[str, Any]:
        return {
            "ingredient_name": self.ingredient.name,
            "quantity": self.quantity,
        }

    def __post_init__(self):
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

    def __post_init__(self):
        self.name = format_option(self.name)
