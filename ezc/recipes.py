from dataclasses import dataclass
from typing import List


@dataclass
class Ingredient:
    name: str
    shelf: str
    price: float
    unite: str = "kg"

    def to_json(self):
        return {
            "name": self.name,
            "shelf": self.shelf,
            "price": self.price,
            "unite": self.unite,
        }


@dataclass
class RecipeElement:
    ingredient: Ingredient
    quantity: int

    def to_json(self):
        return {
            "ingredient_name": self.ingredient.name,
            "quantity": self.quantity,
        }


@dataclass
class Recipe:
    name: str
    ingredients: List[RecipeElement]

    def to_json(self):
        return {
            "name": self.name,
            "ingredients_list": [
                ingredient.to_json() for ingredient in self.ingredients
            ],
        }
