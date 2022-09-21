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

data_iterate_ingredients = [
    (
        "tests/test_excel_factory/excel_files/pates_pesto.xlsx",
        [
            ["Pates", 1],
            ["Pesto", 0.2],
            ["Champignons", 0.4],
            ["Courgettes", 4],
            ["Gruyere", 0.2],
        ],
    )
]
