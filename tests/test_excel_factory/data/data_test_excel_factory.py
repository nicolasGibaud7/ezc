from ezc.recipes import Ingredient, RecipeElement

data_add_element = [
    (["Prix", "Poids", "Unite", "Volume"]),
    (["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]),
]

data_add_ingredient = [
    (["Poulet", "viande", "1", "kg", "8"], 4),
    (["Yaourt", "frais", "0.5", "kg", "4"], 5),
]

data_create_header_row = [
    (["Nom", "Prix", "Unite"]),
    (["NOM", "PRIX", "UNITE"]),
]

data_get_recipe_name = [
    ("tests/test_excel_factory/excel_files/pates_pesto.xlsx", "Pates pesto")
]

data_iterate_recipe_element = [
    (
        "tests/test_excel_factory/excel_files/pates_pesto.xlsx",
        [
            RecipeElement("Pates", 1),
            RecipeElement("Pesto", 0.2),
            RecipeElement("Champignons", 0.4),
            RecipeElement("Courgettes", 4),
            RecipeElement("Gruyere", 0.2),
        ],
    )
]

data_iterate_ingredient = [
    (
        "tests/test_excel_factory/excel_files/add_ingredients.xlsx",
        [
            Ingredient("Chips", "epicerie salee", 12, "kg"),
            Ingredient("Creme fraiche", "frais", 5, "kg"),
            Ingredient("Lait", "frais", 0.8, "kg"),
        ],
    )
]
