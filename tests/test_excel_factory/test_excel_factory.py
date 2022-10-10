import os
from typing import Any, List

import pytest
from ezc.constants import EXCEL_COLUMNS, TITLE_CELL
from ezc.excel_factory import ExcelFactory
from ezc.recipes import Ingredient, RecipeElement
from tests.test_excel_factory.data.data_test_excel_factory import (
    data_add_element,
    data_add_ingredient,
    data_create_header_row,
    data_get_recipe_name,
    data_iterate_ingredient,
    data_iterate_recipe_element,
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


def test_add_title():
    try:
        excel_factory = ExcelFactory("test_add_title.xlsx")
        excel_factory.add_title()

        title_cell = excel_factory.current_sheet[TITLE_CELL]
        assert title_cell.font.bold is True
        assert title_cell.alignment.horizontal == "center"
        assert title_cell.alignment.vertical == "center"
        assert title_cell.border.bottom.style == "thin"
        assert title_cell.border.top.style == "thin"
        assert title_cell.border.left.style == "thin"
        assert title_cell.border.right.style == "thin"
        assert title_cell.value == "Test_add_title"

        other_cell = excel_factory.current_sheet["A1"]
        assert other_cell.font.bold is not True
        assert other_cell.alignment.horizontal != "center"
        assert other_cell.alignment.vertical != "center"
        assert other_cell.border.bottom.style != "thin"
        assert other_cell.border.top.style != "thin"
        assert other_cell.border.left.style != "thin"
        assert other_cell.border.right.style != "thin"

    finally:
        os.remove("test_add_title.xlsx")


@pytest.mark.parametrize("categories", data_create_header_row)
def test_create_header_row(categories: List[str]):
    try:
        excel_factory = ExcelFactory("test_create_header_row.xlsx")
        excel_factory.create_header_row(categories)

        for index, header_column in enumerate(
            EXCEL_COLUMNS[0 : len(categories)]
        ):
            header_cell = excel_factory.current_sheet[f"{header_column}3"]
            assert header_cell.style == "Headline 2"
            assert header_cell.value == categories[index]

    finally:
        os.remove("test_create_header_row.xlsx")


@pytest.mark.parametrize("excel_file, expected_result", data_get_recipe_name)
def test_get_recipe_name(excel_file: str, expected_result: str):
    excel_factory = ExcelFactory(excel_file)
    assert excel_factory.get_recipe_name() == expected_result


@pytest.mark.parametrize(
    "excel_file, expected_result", data_iterate_recipe_element
)
def test_iterate_recipe_element(
    excel_file: str, expected_result: List[RecipeElement]
):
    excel_factory = ExcelFactory(excel_file)
    for index, recipe_element in enumerate(
        excel_factory.iterate_recipe_element()
    ):
        assert recipe_element == expected_result[index]


@pytest.mark.parametrize(
    "excel_file, expected_result", data_iterate_ingredient
)
def test_iterate_ingredient(
    excel_file: str, expected_result: List[Ingredient]
):
    excel_factory = ExcelFactory(excel_file)
    for index, ingredient in enumerate(excel_factory.iterate_ingredient()):
        assert ingredient == expected_result[index]
