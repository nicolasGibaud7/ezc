data_add_ingredient = [
    (
        "concombre",
        "legumes",
        0.8,
        "market",
        "kg",
        {
            "name": "concombre",
            "shelf": "legumes",
            "price": 0.8,
            "category": "market",
            "unite": "kg",
        },
    )
]

data_add_ingredients = [
    (
        "tests/test_public_api/excel_files/add_ingredients.xlsx",
        [
            {
                "name": "chips",
                "shelf": "epicerie salee",
                "price": 12,
                "category": "supermarket",
                "unite": "kg",
            },
            {
                "name": "creme fraiche",
                "shelf": "frais",
                "price": 5,
                "category": "supermarket",
                "unite": "kg",
            },
            {
                "name": "lait",
                "shelf": "frais",
                "price": 0.8,
                "category": "supermarket",
                "unite": "kg",
            },
        ],
    )
]

data_add_recipe = [
    (
        "tests/test_public_api/excel_files/add_recipe.xlsx",
        {
            "name": "riz curry",
            "ingredients_list": [
                {"ingredient_name": "riz", "quantity": 1},
                {"ingredient_name": "courgette", "quantity": 4},
                {"ingredient_name": "champignon", "quantity": 300},
                {"ingredient_name": "creme fraiche", "quantity": 100},
                {"ingredient_name": "soja", "quantity": 1},
            ],
        },
    )
]

data_create_list = [
    (
        ["pates pesto"],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "quantity": 1,
                "unite": "kg",
                "price": 1.1,
            },
            {
                "name": "pesto",
                "shelf": "epicerie salee",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.4,
            },
            {
                "name": "champignon",
                "shelf": "legumes",
                "quantity": 0.4,
                "unite": "kg",
                "price": 0.48,
            },
            {
                "name": "courgette",
                "shelf": "legumes",
                "quantity": 4,
                "unite": "unite",
                "price": 1,
            },
            {
                "name": "gruyere",
                "shelf": "frais",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.5,
            },
        ],
        [],
        [
            {
                "name": "champignon",
                "shelf": "legumes",
                "quantity": 0.4,
                "unite": "kg",
                "price": 0.48,
            },
            {
                "name": "courgette",
                "shelf": "legumes",
                "quantity": 4,
                "unite": "unite",
                "price": 1,
            },
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "quantity": 1,
                "unite": "kg",
                "price": 1.1,
            },
            {
                "name": "pesto",
                "shelf": "epicerie salee",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.4,
            },
            {
                "name": "gruyere",
                "shelf": "frais",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.5,
            },
        ],
    ),
    (
        ["pates pesto", "pates raclettes"],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "quantity": 2,
                "unite": "kg",
                "price": 2.2,
            },
            {
                "name": "pesto",
                "shelf": "epicerie salee",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.4,
            },
            {
                "name": "champignon",
                "shelf": "legumes",
                "quantity": 0.4,
                "unite": "kg",
                "price": 0.48,
            },
            {
                "name": "courgette",
                "shelf": "legumes",
                "quantity": 4,
                "unite": "unite",
                "price": 1,
            },
            {
                "name": "gruyere",
                "shelf": "frais",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.5,
            },
            {
                "name": "raclette",
                "shelf": "frais",
                "quantity": 1,
                "unite": "kg",
                "price": 4,
            },
        ],
        [],
        [
            {
                "name": "champignon",
                "shelf": "legumes",
                "quantity": 0.4,
                "unite": "kg",
                "price": 0.48,
            },
            {
                "name": "courgette",
                "shelf": "legumes",
                "quantity": 4,
                "unite": "unite",
                "price": 1,
            },
        ],
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "quantity": 2,
                "unite": "kg",
                "price": 2.2,
            },
            {
                "name": "pesto",
                "shelf": "epicerie salee",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.4,
            },
            {
                "name": "gruyere",
                "shelf": "frais",
                "quantity": 0.2,
                "unite": "kg",
                "price": 0.5,
            },
            {
                "name": "raclette",
                "shelf": "frais",
                "quantity": 1,
                "unite": "kg",
                "price": 4,
            },
        ],
    ),
]
