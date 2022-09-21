data_add_ingredient_to_json_file = [
    (
        "tests/test_json_utility/json_files/add_ingredient_to_json_file.json",
        "concombre",
        "legumes",
        0.92,
        "kg",
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.92,
                "unite": "kg",
            },
        ],
    )
]

data_add_ingredients_to_json_file = [
    (
        "tests/test_json_utility/json_files/add_ingredients_to_json_file.json",
        [
            ["concombre", "legumes", 0.92, "kg"],
            ["raclette", "fromage", 5.27, "unite"],
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.92,
                "unite": "kg",
            },
            {
                "name": "raclette",
                "shelf": "fromage",
                "price": 5.27,
                "unite": "unite",
            },
        ],
    )
]

data_update_ingredients_in_json_file = [
    (
        "tests/test_json_utility/json_files/update_ingredients_in_json_file.json",
        [
            ["pate", "epicerie salee", 1.1, "kg"],
            ["concombre", "legumes", 0.95, "kg"],
            ["raclette", "fromage", 5.27, "unite"],
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.95,
                "unite": "kg",
            },
            {
                "name": "raclette",
                "shelf": "fromage",
                "price": 5.27,
                "unite": "unite",
            },
        ],
    ),
    (
        "tests/test_json_utility/json_files/update_ingredients_in_json_file.json",
        [
            ["pate", "epicerie salee", 1.1, "kg"],
            ["concombre", "legumes", 0.92, "kg"],
            ["raclette", "fromage", 15.27, "kg"],
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "unite": "kg",
            },
            {
                "name": "concombre",
                "shelf": "legumes",
                "price": 0.92,
                "unite": "kg",
            },
            {
                "name": "raclette",
                "shelf": "fromage",
                "price": 15.27,
                "unite": "kg",
            },
        ],
    ),
]


data_update_ingredient_in_json_file = [
    (
        "tests/test_json_utility/json_files/update_ingredient_in_json_file.json",
        "pate",
        "epicerie salee",
        0.9,
        "kg",
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 0.9,
                "unite": "kg",
            }
        ],
    ),
    (
        "tests/test_json_utility/json_files/update_ingredient_in_json_file.json",
        "pate",
        "epicerie",
        1.3,
        "kg",
        [{"name": "pate", "shelf": "epicerie", "price": 1.3, "unite": "kg"}],
    ),
    (
        "tests/test_json_utility/json_files/update_ingredient_in_json_file.json",
        "pate",
        "epicerie salee",
        1.1,
        "kg",
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
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
                "name": "Pates pesto",
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
        "Pates pesto",
        {
            "name": "Pates pesto",
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
]

data_check_recipe_presence = [
    ("Pates pesto", True),
    ("pates pesto", False),
    ("pates raclettes", True),
    ("PATES RACLETTES", False),
    ("Gratin dauphinois", False),
]

data_check_ingredient_presence = [
    ("eau", True),
    ("gruyere", True),
    ("Eau", False),
    ("raclette", True),
    ("", False),
]

data_get_json_ingredient = [
    ("eau", {"name": "eau", "shelf": "boissons", "price": 0.35, "unite": "l"}),
    (
        "pate",
        {
            "name": "pate",
            "shelf": "epicerie salee",
            "price": 1.1,
            "unite": "kg",
        },
    ),
    (
        "pesto",
        {
            "name": "pesto",
            "shelf": "epicerie salee",
            "price": 2,
            "unite": "kg",
        },
    ),
]
