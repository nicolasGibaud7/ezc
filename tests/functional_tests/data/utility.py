from typing import Any, Dict, List


def generate_add_ingredient_command_parameters(
    name: str,
    shelf: str,
    price: str,
    category: str,
    unite: str,
    config: str,
    log: str,
) -> List[str]:
    return [
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
        f"{config}",
        "--log",
        f"{log}",
    ]


def ingredient_database_representation(
    name: str, shelf: str, price: float, category: str, unite: str
) -> Dict[str, Any]:
    return {
        "name": name,
        "shelf": shelf,
        "price": price,
        "category": category,
        "unite": unite,
    }


def recipe_database_representation(
    name: str, ingredients: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    return [
        {
            "name": name,
            "ingredients_list": [
                {
                    "ingredient_name": ingredient["name"],
                    "quantity": ingredient["quantity"],
                }
                for ingredient in ingredients
            ],
        }
    ]
