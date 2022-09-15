from typing import Any, Dict, List

from ezc.globals import logger


def format_option(option: Any):
    try:
        return option.lower()
    except AttributeError:
        return option


def print_shopping_list(shopping_list: List[Dict[str, Any]]):
    logger.debug("==== Shopping list ====")
    for shopping_element in shopping_list:
        logger.debug(
            f" - {shopping_element['name']} - {shopping_element['shelf']} - {shopping_element['quantity']}({shopping_element['unite']}) - {shopping_element['price']} euros"
        )
