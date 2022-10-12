from ezc.recipes import Ingredient

data_add_ingredient_to_json_file = [
    (
        "tests/test_json_utility/json_files/add_ingredient_to_json_file.json",
        Ingredient("concombre", "legumes", 0.92, "market", "kg").to_json(),
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "category": "supermarket",
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.92,
                "category": "market",
                "unite": "kg",
            },
        ],
    )
]

data_add_ingredients_to_json_file = [
    (
        "tests/test_json_utility/json_files/add_ingredients_to_json_file.json",
        [
            ["concombre", "legumes", 0.92, "market", "kg"],
            ["raclette", "fromage", 5.27, "supermarket", "unite"],
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "category": "supermarket",
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.92,
                "category": "market",
                "unite": "kg",
            },
            {
                "name": "raclette",
                "shelf": "fromage",
                "price": 5.27,
                "category": "supermarket",
                "unite": "unite",
            },
        ],
    )
]

data_update_ingredients_in_json_file = [
    (
        "tests/test_json_utility/json_files/update_ingredients_in_json_file.json",
        [
            ["pate", "epicerie salee", 1.1, "supermarket", "kg"],
            ["concombre", "legumes", 0.95, "market", "kg"],
            ["raclette", "fromage", 5.27, "supermarket", "unite"],
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "category": "supermarket",
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.95,
                "category": "market",
                "unite": "kg",
            },
            {
                "name": "raclette",
                "shelf": "fromage",
                "price": 5.27,
                "category": "supermarket",
                "unite": "unite",
            },
        ],
    ),
    (
        "tests/test_json_utility/json_files/update_ingredients_in_json_file.json",
        [
            ["pate", "epicerie salee", 1.1, "supermarket", "kg"],
            ["concombre", "legumes", 0.92, "market", "kg"],
            ["raclette", "fromage", 15.27, "supermarket", "kg"],
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "category": "supermarket",
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.92,
                "category": "market",
                "unite": "kg",
            },
            {
                "name": "raclette",
                "shelf": "fromage",
                "price": 15.27,
                "category": "supermarket",
                "unite": "kg",
            },
        ],
    ),
]


data_update_ingredient_in_json_file = [
    (
        "tests/test_json_utility/json_files/update_ingredient_in_json_file.json",
        Ingredient(
            "pate", "epicerie salee", 0.9, "supermarket", "kg"
        ).to_json(),
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 0.9,
                "category": "supermarket",
                "unite": "kg",
            }
        ],
    ),
    (
        "tests/test_json_utility/json_files/update_ingredient_in_json_file.json",
        Ingredient("pate", "epicerie", 1.3, "supermarket", "kg").to_json(),
        [
            {
                "name": "pate",
                "shelf": "epicerie",
                "price": 1.3,
                "category": "supermarket",
                "unite": "kg",
            }
        ],
    ),
    (
        "tests/test_json_utility/json_files/update_ingredient_in_json_file.json",
        Ingredient(
            "pate", "epicerie salee", 1.1, "supermarket", "kg"
        ).to_json(),
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "category": "supermarket",
                "unite": "kg",
            }
        ],
    ),
]

data_add_recipe_to_json_file = [
    (
        "tests/test_json_utility/json_files/add_recipe_to_json_file.json",
        "pates raclettes",
        [
            {"ingredient_name": "pate", "quantity": 1},
            {"ingredient_name": "raclette", "quantity": 1},
        ],
        [
            {
                "name": "pates pesto",
                "ingredients_list": [
                    {"ingredient_name": "pate", "quantity": 1},
                    {"ingredient_name": "pesto", "quantity": 0.2},
                    {"ingredient_name": "champignon", "quantity": 0.4},
                    {"ingredient_name": "courgette", "quantity": 4},
                    {"ingredient_name": "gruyere", "quantity": 0.2},
                ],
            },
            {
                "name": "pates raclettes",
                "ingredients_list": [
                    {"ingredient_name": "pate", "quantity": 1},
                    {"ingredient_name": "raclette", "quantity": 1},
                ],
            },
        ],
    )
]

data_get_json_recipe = [
    (
        "pates pesto",
        {
            "name": "pates pesto",
            "ingredients_list": [
                {"ingredient_name": "pate", "quantity": 1},
                {"ingredient_name": "pesto", "quantity": 0.2},
                {"ingredient_name": "champignon", "quantity": 0.4},
                {"ingredient_name": "courgette", "quantity": 4},
                {"ingredient_name": "gruyere", "quantity": 0.2},
            ],
        },
    ),
    (
        "pates raclettes",
        {
            "name": "pates raclettes",
            "ingredients_list": [
                {"ingredient_name": "pate", "quantity": 1},
                {"ingredient_name": "raclette", "quantity": 1},
            ],
        },
    ),
    ("fgdskfgdsklgf", None),
]

data_check_recipe_presence = [
    ("Pates pesto", False),
    ("pates pesto", True),
    ("pates raclettes", True),
    ("PATES RACLETTES", False),
    ("Gratin dauphinois", False),
]

data_check_ingredient_presence = [
    ("eau", "tests/json_files/ingredients.json", True),
    ("gruyere", "tests/json_files/ingredients.json", True),
    ("Eau", "tests/json_files/ingredients.json", False),
    ("raclette", "tests/json_files/ingredients.json", True),
    ("", "tests/json_files/ingredients.json", False),
]

data_get_json_ingredient = [
    (
        "eau",
        {
            "name": "eau",
            "shelf": "boissons",
            "price": 0.35,
            "category": "supermarket",
            "unite": "l",
        },
    ),
    (
        "pate",
        {
            "name": "pate",
            "shelf": "epicerie salee",
            "price": 1.1,
            "category": "supermarket",
            "unite": "kg",
        },
    ),
    (
        "pesto",
        {
            "name": "pesto",
            "shelf": "epicerie salee",
            "price": 2,
            "category": "supermarket",
            "unite": "kg",
        },
    ),
    ("fgdskgfslg", None),
]
