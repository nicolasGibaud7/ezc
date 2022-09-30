from dataclasses import dataclass
from typing import Any, Dict, List

from ezc.exceptions import NotMatchingException
from ezc.recipes import Ingredient, RecipeElement


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

    def __post_init__(self):
        if self.ingredient.name != self.recipe_element.ingredient_name:
            raise NotMatchingException(
                f"Ingredient {self.ingredient.name} different of {self.recipe_element.ingredient_name}"
            )


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
        return "\n".join([f"{element}" for element in self.elements])
