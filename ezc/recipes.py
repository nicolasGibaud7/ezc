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


@dataclass
class ShoppingElement:
    ingredient: Ingredient
    recipe_element: RecipeElement

    @property
    def price(self):
        return self.recipe_element.quantity * self.ingredient.price

    def to_json(self) -> Dict[str, Any]:
        return {
            "name": self.ingredient.name,
            "shelf": self.ingredient.shelf,
            "quantity": self.recipe_element.quantity,
            "unite": self.ingredient.unite,
            "price": self.price,
        }

    def __repr__(self) -> str:
        return f"{self.ingredient.name} : {self.ingredient.shelf} - {self.recipe_element.quantity} {self.ingredient.unite} - {self.price} euros"


@dataclass
class ShoppingList:  # TODO Add inheritance to List instead of having a list as attribute
    elements: List[ShoppingElement]

    def to_json(self) -> List[Dict[str, Any]]:
        return [element.to_json() for element in self.elements]

    def add_or_update_element(self, shopping_element: ShoppingElement):
        if self.check_element_presence(shopping_element):
            self.update_element(shopping_element)
        else:
            self.elements.append(shopping_element)

    def check_element_presence(self, element: ShoppingElement):
        return any(
            [
                element
                for shopping_element in self.elements
                if element.ingredient == shopping_element.ingredient
            ]
        )

    def update_element(self, shopping_element: ShoppingElement):
        for index, element in enumerate(self.elements):
            if element.ingredient == shopping_element.ingredient:
                self.elements[
                    index
                ].recipe_element.quantity += (
                    shopping_element.recipe_element.quantity
                )

    def length(self):
        return len(self.elements)

    def __repr__(self) -> str:
        str_list = ["==== Shopping list ===="]
        for element in self.elements:
            str_list.append(f"{element}")
        return "\n".join(str_list)
