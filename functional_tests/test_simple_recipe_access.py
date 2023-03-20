from .base import FunctionalTest


class RecipeAccessTest(FunctionalTest):
    def test_access_recipes_page_and_see_recipes_information(self):

        # User goes to the home page
        self.browser.get(self.live_server_url)

        self.wait_for_page("Welcome to ezcourses")

        # User clicks on the recipes button
        self.browser.find_element("id", "id_recipes_link").click()

        # User sees that he was redirected to the recipes page
        self.wait_for_page("Recipes")

        # User sees recipes table
        recipes_table = self.browser.find_element("id", "id_recipes_table")
        self.assertNotEqual(
            recipes_table.find_elements("css selector", "div"),
            [],
            "The recipes table is empty",
        )

        # User sees tomato soup recipe
        self.assertIn("Tomato soup", recipes_table.text)

        # User check if the recipe contains the ingredients and their quantities
        tomato_soup_recipe_element = [
            recipe
            for recipe in recipes_table.find_elements(
                "xpath", '//div[@class="card"]'
            )
            if "Tomato soup" in recipe.text
        ][0]

        self.assertIn(
            "1 ingredients",
            tomato_soup_recipe_element.text,
            tomato_soup_recipe_element.text,
        )

    def test_access_recipe_details(self):

        # User goes to the recipes page
        self.browser.get(self.live_server_url + "/recipes/")
        self.wait_for_page("Recipes")

        # User see recipes table
        recipes_table = self.browser.find_element("id", "id_recipes_table")
        self.assertNotEqual(
            recipes_table.find_elements("css selector", "div"),
            [],
            "The recipes table is empty",
        )

        # User clicks on the tomato soup recipe
        recipes_table.find_element("id", "id_details_button_1").click()

        # User sees that he was redirected to the recipe details page
        self.wait_for_page("Recipe details")

        # User check recipe details on the page
        self.assertIn(
            "Tomato soup",
            self.browser.find_element("id", "id_recipe_name").text,
        )

        self.assertIn(
            "Tomato",
            self.browser.find_element("id", "id_ingredient_name").text,
        )
        self.assertIn(
            "3.00",
            self.browser.find_element("id", "id_ingredient_quantity").text,
        )
        self.assertIn(
            "Kilogram (Kg)",
            self.browser.find_element("id", "id_ingredient_unit").text,
        )
        self.assertIn(
            "3.90",
            self.browser.find_element("id", "id_ingredient_price").text,
        )
