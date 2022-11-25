from typing import Any, Dict, List

from data.utility import (
    generate_add_ingredient_command_parameters,
    ingredient_database_representation,
)


def courgette_missing_name_param(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "courgette", "LEGUMES", "0.8", "market", "kg", config, log
    )[2:]


def carrot_bad_category(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "carrot", "LEGUMES", "1.21", "mrket", "kg", config, log
    )


def carrot(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "carrot", "LEGUMES", "1.21", "market", "kg", config, log
    )


def carrot_representation() -> Dict[str, Any]:
    return ingredient_database_representation(
        "carrot", "legumes", 1.21, "market", "kg"
    )


def lower_price_carrot(config: str, log: str) -> List[str]:
    return generate_add_ingredient_command_parameters(
        "carrot", "LEGUMES", "0.99", "market", "kg", config, log
    )


def lower_price_carrot_representation() -> Dict[str, Any]:
    return ingredient_database_representation(
        "carrot", "legumes", 0.99, "market", "kg"
    )
