from .base import FunctionalTest

MAX_WAIT = 10


class IngredientAccessTest(FunctionalTest):
    def test_access_ingredients_page_and_see_ingredients_information(self):

        # User goes to the home page
        self.browser.get(self.live_server_url)

        self.wait_for_page("Welcome to ezcourses")

        # User clicks on the ingredients button
        self.browser.find_element("id", "id_ingredients_button").click()

        # User sees that he was redirected to the ingredients page
        self.wait_for_page("Ingredients")

        # User sees ingredients table
        ingredients_table = self.browser.find_element(
            "id", "id_ingredients_table"
        )
        self.assertNotEqual(
            ingredients_table.find_elements("css selector", "tr"),
            [],
            "The ingredients table is empty",
        )

        # User sees tomato ingredient
        tomato_ingredient_element = [
            ingredient
            for ingredient in ingredients_table.find_elements(
                "css selector", "tr"
            )
            if "Tomato" in ingredient.text
        ][0]

        self.assertIn(
            "Tomato",
            tomato_ingredient_element.text,
        )
        self.assertIn(
            "Fruits and vegetables",
            tomato_ingredient_element.text,
        )
        self.assertIn(
            "Market",
            tomato_ingredient_element.text,
        )
        self.assertIn(
            "Kilogram (Kg)",
            tomato_ingredient_element.text,
        )
        self.assertIn("1.30 €", tomato_ingredient_element.text)

    def test_access_ingredients_details(self):

        # User goes to the ingredients page
        self.browser.get(self.live_server_url + "/ingredients/")

        self.wait_for_page("Ingredients")

        # User sees ingredients table
        ingredients_table = self.browser.find_element(
            "id", "id_ingredients_table"
        )

        # User clicks on the tomato ingredient
        ingredients_table.find_element("id", "id_details_button_1").click()

        # User sees that he was redirected to the ingredient details page
        self.wait_for_page("Ingredient details")

        # User check the ingredients details
        self.assertIn(
            "Tomato",
            self.browser.find_element("id", "id_ingredient_name").text,
        )
        self.assertIn(
            "Fruits and vegetables",
            self.browser.find_element("id", "id_ingredient_shelf").text,
        )
        self.assertIn(
            "Market",
            self.browser.find_element("id", "id_ingredient_category").text,
        )
        self.assertIn(
            "Kilogram (Kg)",
            self.browser.find_element("id", "id_ingredient_unit").text,
        )
        self.assertIn(
            "1.30",
            self.browser.find_element("id", "id_ingredient_price").text,
        )

    def test_access_unknown_ingredient_details(self):

        # User tries to access manually to the ingredients details page of an unknown ingredient
        self.browser.get(self.live_server_url + "/ingredients/999/")

        # User sees that he was redirected to the ingredients page
        self.wait_for_page("Ingredients")
