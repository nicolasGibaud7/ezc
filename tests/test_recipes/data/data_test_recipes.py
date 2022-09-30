from ezc.recipes import Ingredient, RecipeElement
from ezc.shopping import ShoppingElement

data_test_ingredient = [
    (
        "courgette",
        "legumes",
        0.78,
        "kg",
        {
            "name": "courgette",
            "shelf": "legumes",
            "price": 0.78,
            "unite": "kg",
        },
    ),
    (
        "caroTte",
        "legumes",
        1.2,
        "kg",
        {
            "name": "carotte",
            "shelf": "legumes",
            "price": 1.2,
            "unite": "kg",
        },
    ),
    (
        "YaOuRt",
        "FRAIs",
        3.5,
        "Kg",
        {
            "name": "yaourt",
            "shelf": "frais",
            "price": 3.5,
            "unite": "kg",
        },
    ),
]

data_test_recipe_element = [
    (
        "courgette",
        3,
        {"ingredient_name": "courgette", "quantity": 3},
    ),
    (
        "caroTte",
        1,
        {"ingredient_name": "carotte", "quantity": 1},
    ),
    (
        "YaOuRt",
        0,
        {"ingredient_name": "yaourt", "quantity": 0},
    ),
]

data_test_recipe = [
    (
        "pates raclette",
        [
            RecipeElement("pates", quantity=1),
            RecipeElement("raclette", quantity=1),
        ],
        {
            "name": "pates raclette",
            "ingredients_list": [
                {"ingredient_name": "pates", "quantity": 1},
                {"ingredient_name": "raclette", "quantity": 1},
            ],
        },
    ),
    (
        "riZ Curry",
        [
            RecipeElement("RIZ", quantity=1),
            RecipeElement("courgetTes", quantity=2),
            RecipeElement("champignons", quantity=1),
            RecipeElement("curry", quantity=10),
            RecipeElement("creme fraiche", quantity=1),
        ],
        {
            "name": "riz curry",
            "ingredients_list": [
                {"ingredient_name": "riz", "quantity": 1},
                {"ingredient_name": "courgettes", "quantity": 2},
                {"ingredient_name": "champignons", "quantity": 1},
                {"ingredient_name": "curry", "quantity": 10},
                {"ingredient_name": "creme fraiche", "quantity": 1},
            ],
        },
    ),
]

data_test_shopping_element = [
    (
        Ingredient("courgette", "legumes", 1.1, "kg"),
        RecipeElement("courgette", 3.7),
        4.07,
        {
            "name": "courgette",
            "shelf": "legumes",
            "quantity": 3.7,
            "unite": "kg",
            "price": 4.07,
        },
    ),
    (
        Ingredient("lait", "frais", 0.95, "l"),
        RecipeElement("lait", 1.2),
        1.14,
        {
            "name": "lait",
            "shelf": "frais",
            "quantity": 1.2,
            "unite": "l",
            "price": 1.14,
        },
    ),
    (
        Ingredient("courgettes", "frais", 1.1, "kg"),
        RecipeElement("carottes", 2),
        0,
        {},
    ),
]

data_test_shopping_list = [
    (
        [
            ShoppingElement(
                Ingredient("courgette", "legumes", 1.1, "kg"),
                RecipeElement("courgette", 3.7),
            ),
            ShoppingElement(
                Ingredient("lait", "frais", 0.95, "l"),
                RecipeElement("lait", 1.2),
            ),
        ],
        [
            {
                "name": "courgette",
                "shelf": "legumes",
                "quantity": 3.7,
                "unite": "kg",
                "price": 4.07,
            },
            {
                "name": "lait",
                "shelf": "frais",
                "quantity": 1.2,
                "unite": "l",
                "price": 1.14,
            },
        ],
    )
]

data_test_shopping_list_add_or_update_element = [
    (
        [
            ShoppingElement(
                Ingredient("courgette", "legumes", 1.1, "kg"),
                RecipeElement("courgette", 3.7),
            ),
            ShoppingElement(
                Ingredient("lait", "frais", 0.95, "l"),
                RecipeElement("lait", 1.2),
            ),
        ],
        ShoppingElement(
            Ingredient("carotte", "legumes", 1.2, "kg"),
            RecipeElement("carotte", 1),
        ),
        1,
    ),
    (
        [
            ShoppingElement(
                Ingredient("courgette", "legumes", 1.1, "kg"),
                RecipeElement("courgette", 3.5),
            ),
            ShoppingElement(
                Ingredient("lait", "frais", 0.95, "l"),
                RecipeElement("lait", 1.2),
            ),
        ],
        ShoppingElement(
            Ingredient("courgette", "legumes", 1.1, "kg"),
            RecipeElement("courgette", 3),
        ),
        6.5,
    ),
]
