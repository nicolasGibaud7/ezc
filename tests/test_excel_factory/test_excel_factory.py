import os
from typing import Any, List

import pytest
from ezc.constants import EXCEL_COLUMNS
from ezc.excel_factory import ExcelFactory
from tests.test_excel_factory.data.data_test_excel_factory import (
    data_add_element,
    data_add_ingredient,
)


@pytest.mark.parametrize("element_information", data_add_element)
def test_add_element(element_information: List[str]):
    try:
        excel_factory = ExcelFactory("test_add_element.xlsx")

        excel_factory.add_element(element_information)

        for index, element in enumerate(element_information):
            assert (
                excel_factory.current_sheet[f"{EXCEL_COLUMNS[index]}1"].value
                == element
            )
    finally:
        os.remove("test_add_element.xlsx")


@pytest.mark.parametrize(
    "ingredient_information, row_index", data_add_ingredient
)
def test_add_ingredient(ingredient_information: List[str], row_index: int):
    try:
        excel_factory = ExcelFactory("test_add_ingredient.xlsx")

        excel_factory.add_ingredient(ingredient_information, row_index)

        for index, element in enumerate(ingredient_information):
            assert (
                excel_factory.current_sheet[
                    f"{EXCEL_COLUMNS[index]}{row_index}"
                ].value
                == element
            )
            assert (
                excel_factory.current_sheet[
                    f"{EXCEL_COLUMNS[index]}{row_index+1}"
                ].value
                != element
            )

    finally:
        os.remove("test_add_ingredient.xlsx")
