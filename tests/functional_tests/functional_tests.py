import pytest
from click.testing import CliRunner

from ezc.cli import add_ingredient
from tests.functional_tests.data.data_functional_tests import (
    data_func_add_ingredient,
)

CONFIG_FILE = "tests/functional_tests/functional_tests_config.ini"
LOG_STATE = "True"


@pytest.mark.parametrize(
    "name, shelf, price, category, unite", data_func_add_ingredient
)
def test_add_ingredient(
    name: str,
    shelf: str,
    price: str,
    category: str,
    unite: str,
):
    runner = CliRunner()
    result = runner.invoke(
        add_ingredient,
        [
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
            CONFIG_FILE,
            "--log",
            LOG_STATE,
        ],
    )
    print(result.output)
    assert result.exit_code == 0
