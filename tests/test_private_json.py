import json

import pytest
from ezc.json_utility import (
    _add_json_element_to_json_file,
    _add_json_elements_to_json_file,
    _check_json_element_presence,
    _get_json_content_file_with_added_element,
    _get_json_content_file_with_added_elements,
    _update_element_in_json_file,
)

from test_json_utility.data.data_test_private_json import (
    data_add_json_element_to_json_file,
    data_add_json_elements_to_json_file,
    data_check_json_element_presence,
    data_get_json_content_file_with_added_element,
    data_get_json_content_file_with_added_elements,
    data_update_element_in_json_file,
)


@pytest.mark.parametrize(
    "element_identifier, identifier_attribute, json_filename, expected_result",
    data_check_json_element_presence,
)
def test_check_json_element_presence(
    element_identifier, identifier_attribute, json_filename, expected_result
):
    assert (
        _check_json_element_presence(
            element_identifier=element_identifier,
            identifier_attribute=identifier_attribute,
            json_filename=json_filename,
        )
        is expected_result
    )


@pytest.mark.parametrize(
    "json_filename, element, expected_result",
    data_get_json_content_file_with_added_element,
)
def test_get_json_content_file_with_added_element(
    json_filename, element, expected_result
):
    assert (
        _get_json_content_file_with_added_element(
            json_filename=json_filename, element=element
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "json_filename, new_element, identifier_attribute, expected_result",
    data_update_element_in_json_file,
)
def test_update_element_in_json_file(
    json_filename, new_element, identifier_attribute, expected_result
):
    _update_element_in_json_file(
        json_filename, new_element, identifier_attribute
    )
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result


@pytest.mark.parametrize(
    "json_filename, elements, expected_result",
    data_get_json_content_file_with_added_elements,
)
def test_get_json_content_file_with_added_elements(
    json_filename, elements, expected_result
):
    assert (
        _get_json_content_file_with_added_elements(json_filename, elements)
        == expected_result
    )


@pytest.mark.parametrize(
    "json_filename, elements, expected_result",
    data_add_json_elements_to_json_file,
)
def test_add_json_elements_to_json_file(
    json_filename, elements, expected_result
):
    with open(json_filename, "r") as json_file:
        original_json_content = json.load(json_file)

    _add_json_elements_to_json_file(json_filename, elements)
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result

    with open(json_filename, "w") as json_file:
        json.dump(original_json_content, json_file)


@pytest.mark.parametrize(
    "json_filename, element, expected_result",
    data_add_json_element_to_json_file,
)
def test_add_json_element_to_json_file(
    json_filename, element, expected_result
):
    with open(json_filename, "r") as json_file:
        original_json_content = json.load(json_file)

    _add_json_element_to_json_file(json_filename, element)
    with open(json_filename, "r") as json_file:
        json_content = json.load(json_file)
    assert json_content == expected_result

    with open(json_filename, "w") as json_file:
        json.dump(original_json_content, json_file)
