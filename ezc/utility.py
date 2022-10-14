from typing import Any


def format_option(option: Any):
    try:
        return option.lower()
    except AttributeError:
        return option
