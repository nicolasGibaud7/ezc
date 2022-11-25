from typing import Any, Dict, List

from data.utility import (
    generate_add_ingredient_command_parameters,
    ingredient_database_representation,
    recipe_database_representation,
)


def risotto_representation() -> List[Dict[str, Any]]:
    return recipe_database_representation(
        "risotto",
        [
            {"name": "round rice", "quantity": 1},
            {"name": "courgette", "quantity": 1.5},
            {"name": "onion", "quantity": 2},
            {"name": "parmesan", "quantity": 0.1},
        ],
    )


def round_rice(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "round rice", "EPICERIE_SALEE", "1", "supermarket", "kg", config, log
    )


def round_rice_representation() -> Dict[str, Any]:
    return ingredient_database_representation(
        "round rice", "epicerie_salee", 1, "supermarket", "kg"
    )


def courgette(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "courgette", "LEGUMES", "0.8", "market", "kg", config, log
    )


def courgette_representation() -> Dict[str, Any]:
    return ingredient_database_representation(
        "courgette", "legumes", 0.8, "market", "kg"
    )


def onion(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "onion", "LEGUMES", "0.95", "market", "kg", config, log
    )


def onion_representation() -> Dict[str, Any]:
    return ingredient_database_representation(
        "onion", "legumes", 0.95, "market", "kg"
    )


def parmesan(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "parmesan", "FRAIS", "10.28", "supermarket", "kg", config, log
    )


def parmesan_representation() -> Dict[str, Any]:
    return ingredient_database_representation(
        "parmesan", "frais", 10.28, "supermarket", "kg"
    )
