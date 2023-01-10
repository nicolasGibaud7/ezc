from typing import Any, List, Tuple, Union

FROZEN_FOOD_SHOPPING_LIST_FILENAME = "frozen_food_list.xlsx"
SUPERMARKET_SHOPPING_LIST_FILENAME = "supermarket_list.xlsx"
MARKET_SHOPPING_LIST_FILENAME = "market_list.xlsx"

FROZEN_FOOD_EXPECTED_RESULT = [("A4", None)]

SUPERMARKET_EXPECTED_RESULT = [
    ("A4", "round rice"),
    ("B4", "epicerie_salee"),
    ("C4", "1"),
    ("D4", "kg"),
    ("E4", "1"),
    ("A5", "parmesan"),
    ("B5", "frais"),
    ("C5", "0.1"),
    ("D5", "kg"),
    ("E5", "1.028"),
    ("A6", "pasta"),
    ("B6", "epicerie_salee"),
    ("C6", "1"),
    ("D6", "kg"),
    ("E6", "2.4"),
    ("A7", "gruyere"),
    ("B7", "frais"),
    ("C7", "0.1"),
    ("D7", "kg"),
    ("E7", "0.895"),
    ("A8", "pesto"),
    ("B8", "epicerie_salee"),
    ("C8", "0.1"),
    ("D8", "kg"),
    ("E8", "1.162"),
]

MARKET_EXPECTED_RESULT = [
    ("A4", "courgette"),
    ("B4", "legumes"),
    ("C4", "2.3"),
    ("D4", "kg"),
    ("E4", "1.8399999999999999"),
    ("A5", "onion"),
    ("B5", "legumes"),
    ("C5", "4"),
    ("D5", "kg"),
    ("E5", "3.8"),
]


def get_associate_expected_result(
    shopping_list_name: str,
) -> List[Union[Tuple[str, str], Any]]:
    if shopping_list_name == "frozen_food_list.xlsx":
        return FROZEN_FOOD_EXPECTED_RESULT
    elif shopping_list_name == "supermarket_list.xlsx":
        return SUPERMARKET_EXPECTED_RESULT
    elif shopping_list_name == "market_list.xlsx":
        return MARKET_EXPECTED_RESULT
    else:
        return []
