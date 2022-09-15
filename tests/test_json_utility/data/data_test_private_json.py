data_check_json_element_presence = [
    ("pate", "name", "tests/json_files/json_database.json", True),
    ("courgette", "name", "tests/json_files/json_database.json", True),
    (1.1, "price", "tests/json_files/json_database.json", True),
    ("legumes", "shelf", "tests/json_files/json_database.json", True),
    (0.25, "price", "tests/json_files/json_database.json", True),
    ("Pate", "name", "tests/json_files/json_database.json", False),
    ("COURGETTE", "name", "tests/json_files/json_database.json", False),
    ("courgettE", "name", "tests/json_files/json_database.json", False),
    ("courgette", "shelf", "tests/json_files/json_database.json", False),
    ("0.25", "price", "tests/json_files/json_database.json", False),
    ("bztrck", "name", "tests/json_files/json_database.json", False),
    (15185613, "price", "tests/json_files/json_database.json", False),
    (0, "price", "tests/json_files/json_database.json", False),
]

data_get_json_content_file_with_added_element = [
    (
        "tests/test_json_utility/json_files/short_database.json",
        {"name": "poulet", "unite": "kg"},
        [{"name": "pate", "unite": "kg"}, {"name": "poulet", "unite": "kg"}],
    ),
    (
        "tests/test_json_utility/json_files/short_database.json",
        {"name": "poulet", "unite": "kg"},
        [{"name": "pate", "unite": "kg"}, {"name": "poulet", "unite": "kg"}],
    ),
]

data_update_element_in_json_file = [
    (
        "tests/test_json_utility/json_files/update_element_database.json",
        {
            "name": "pate",
            "shelf": "epicerie salee",
            "price": 1.4,
            "unite": "kg",
        },
        "name",
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.4,
                "unite": "kg",
            },
            {
                "name": "pesto",
                "shelf": "epicerie salee",
                "price": 2,
                "unite": "kg",
            },
            {
                "name": "champignon",
                "shelf": "legumes",
                "price": 1.2,
                "unite": "kg",
            },
            {
                "name": "courgette",
                "shelf": "legumes",
                "price": 0.25,
                "unite": "unite",
            },
            {"name": "gruyere", "shelf": "frais", "price": 2.5, "unite": "kg"},
            {"name": "eau", "shelf": "boissons", "price": 0.35, "unite": "l"},
        ],
    ),
    (
        "tests/test_json_utility/json_files/update_element_database.json",
        {
            "name": "pate",
            "shelf": "epicerie salee",
            "price": 1.1,
            "unite": "kg",
        },
        "name",
        [
            {
                "name": "pate",
                "shelf": "epicerie salee",
                "price": 1.1,
                "unite": "kg",
            },
            {
                "name": "pesto",
                "shelf": "epicerie salee",
                "price": 2,
                "unite": "kg",
            },
            {
                "name": "champignon",
                "shelf": "legumes",
                "price": 1.2,
                "unite": "kg",
            },
            {
                "name": "courgette",
                "shelf": "legumes",
                "price": 0.25,
                "unite": "unite",
            },
            {"name": "gruyere", "shelf": "frais", "price": 2.5, "unite": "kg"},
            {"name": "eau", "shelf": "boissons", "price": 0.35, "unite": "l"},
        ],
    ),
]

data_get_json_content_file_with_added_elements = [
    (
        "tests/test_json_utility/json_files/get_json_content_with_added_elements.json",
        [
            {"name": "courgette", "unite": "kg"},
            {"name": "pomme", "unite": "kg"},
            {"name": "abricot", "unite": "kg"},
        ],
        [
            {"name": "pate", "unite": "kg"},
            {"name": "courgette", "unite": "kg"},
            {"name": "pomme", "unite": "kg"},
            {"name": "abricot", "unite": "kg"},
        ],
    )
]

data_add_json_elements_to_json_file = [
    (
        "tests/test_json_utility/json_files/add_json_elements_to_json_file.json",
        [
            {"name": "courgette", "unite": "kg"},
            {"name": "pomme", "unite": "kg"},
            {"name": "abricot", "unite": "kg"},
        ],
        [
            {"name": "pate", "unite": "kg"},
            {"name": "courgette", "unite": "kg"},
            {"name": "pomme", "unite": "kg"},
            {"name": "abricot", "unite": "kg"},
        ],
    )
]

data_add_json_element_to_json_file = [
    (
        "tests/test_json_utility/json_files/add_json_element_to_json_file.json",
        {"name": "concombre", "unite": "kg"},
        [
            {"name": "pate", "unite": "kg"},
            {"name": "concombre", "unite": "kg"},
        ],
    )
]
