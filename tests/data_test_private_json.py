data_check_json_element_presence = [
    ("pate", "name", "json_files/json_database.json", True),
    ("courgette", "name", "json_files/json_database.json", True),
    (1.1, "price", "json_files/json_database.json", True),
    ("legumes", "shelf", "json_files/json_database.json", True),
    (0.25, "price", "json_files/json_database.json", True),
    ("Pate", "name", "json_files/json_database.json", False),
    ("COURGETTE", "name", "json_files/json_database.json", False),
    ("courgettE", "name", "json_files/json_database.json", False),
    ("courgette", "shelf", "json_files/json_database.json", False),
    ("0.25", "price", "json_files/json_database.json", False),
    ("bztrck", "name", "json_files/json_database.json", False),
    (15185613, "price", "json_files/json_database.json", False),
    (0, "price", "json_files/json_database.json", False),
]

data_get_json_content_file_with_added_element = [
    (
        "json_files/short_database.json",
        {"name": "poulet", "unite": "kg"},
        [{"name": "pate", "unite": "kg"}, {"name": "poulet", "unite": "kg"}],
    ),
    (
        "json_files/short_database.json",
        {"name": "poulet", "unite": "kg"},
        [{"name": "pate", "unite": "kg"}, {"name": "poulet", "unite": "kg"}],
    ),
]

data_update_element_in_json_file = [
    (
        "json_files/update_element_database.json",
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
        "json_files/update_element_database.json",
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
        "json_files/get_json_content_with_added_elements.json",
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
        "json_files/add_json_elements_to_json_file.json",
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
        "json_files/add_json_element_to_json_file.json",
        {"name": "concombre", "unite": "kg"},
        [
            {"name": "pate", "unite": "kg"},
            {"name": "concombre", "unite": "kg"},
        ],
    )
]
