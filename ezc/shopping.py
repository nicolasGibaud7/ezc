from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from ezc.constants import (
    FROZEN_FOOD_CATEGORY,
    MARKET_CATEGORY,
    SUPERMARKET_CATEGORY,
)
from ezc.recipes import Ingredient


@dataclass
class ShoppingElement:
    """
    Represent a shopping element of a shopping list. It contains information
    about the ingredient and it's quantity o buy


    """

    ingredient: Ingredient
    quantity: float

    @property
    def price(self):
        return self.quantity * self.ingredient.price

    def to_json(self) -> Dict[str, Any]:
        return {
            "name": self.ingredient.name,
            "shelf": self.ingredient.shelf,
            "quantity": self.quantity,
            "unite": self.ingredient.unite,
            "price": self.price,
        }

    def __repr__(self) -> str:
        return (
            f"{self.ingredient.name} : {self.ingredient.shelf} -"
            f"{self.quantity} {self.ingredient.unite} - {self.price} euros"
        )


@dataclass
class ShoppingList:  # TODO Add inheritance to List instead of having a list as attribute
    """
    Contains a list of shopping element to buy. And provide tools to interact
    with by adding or updating elements.

    """

    elements: List[ShoppingElement]

    @property
    def frozen_food(self) -> ShoppingList:
        return self._create_list_for_category(FROZEN_FOOD_CATEGORY)

    @property
    def market(self) -> ShoppingList:
        return self._create_list_for_category(MARKET_CATEGORY)

    @property
    def supermarket(self) -> ShoppingList:
        return self._create_list_for_category(SUPERMARKET_CATEGORY)

    def to_json(self) -> List[Dict[str, Any]]:
        return [element.to_json() for element in self.elements]

    def add_or_update_element(self, shopping_element: ShoppingElement):
        """Add an element in the shopping list if it's not already in the
        list, else, update the element quantity.

        Args:
            shopping_element (ShoppingElement): shopping element object to add
            or update.
        """
        if self.check_element_presence(shopping_element):
            self.update_element(shopping_element)
        else:
            self.elements.append(shopping_element)

    def check_element_presence(self, element: ShoppingElement):
        return any(
            [
                True
                for shopping_element in self.elements
                if element.ingredient == shopping_element.ingredient
            ]
        )

    def update_element(self, shopping_element: ShoppingElement):
        for index, element in enumerate(self.elements):
            if element.ingredient == shopping_element.ingredient:
                self.elements[index].quantity += shopping_element.quantity

    def length(self):
        return len(self.elements)

    def _create_list_for_category(self, category: str) -> ShoppingList:
        return ShoppingList(
            [
                shopping_element
                for shopping_element in self.elements
                if shopping_element.ingredient.category == category
            ]
        )

    def __repr__(self) -> str:
        return "\n".join([f"{element}" for element in self.elements])
