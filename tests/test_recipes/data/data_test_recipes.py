from ezc.recipes import Ingredient, RecipeElement

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
        Ingredient("courgette", "legumes", 0.78, "kg"),
        3,
        {"ingredient_name": "courgette", "quantity": 3},
    ),
    (
        Ingredient("caroTte", "legumes", 1.2, "kg"),
        1,
        {"ingredient_name": "carotte", "quantity": 1},
    ),
    (
        Ingredient("YaOuRt", "FRAIs", 3.5, "kg"),
        0,
        {"ingredient_name": "yaourt", "quantity": 0},
    ),
]

data_test_recipe = [
    (
        "pates raclette",
        [
            RecipeElement(
                Ingredient("pates", "epicerie salee", 0.8, "kg"), quantity=1
            ),
            RecipeElement(
                Ingredient("raclette", "fromage", 4.6, "kg"), quantity=1
            ),
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
            RecipeElement(
                Ingredient("RIZ", "epicerie salee", 0.8, "kg"), quantity=1
            ),
            RecipeElement(
                Ingredient("courgetTes", "legumes", 0.78, "kg"), quantity=2
            ),
            RecipeElement(
                Ingredient("champignons", "leGumes", 0.55, "kg"), quantity=1
            ),
            RecipeElement(
                Ingredient("curry", "epicerie salee", 0.06, "g"), quantity=10
            ),
            RecipeElement(
                Ingredient("creme fraiche", "frais", 2.5, "kg"), quantity=1
            ),
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
