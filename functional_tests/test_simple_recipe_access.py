from list_generation.models import Recipe

from .base import FunctionalTest


class RecipeAccessTest(FunctionalTest):
    def test_access_recipes_page_and_see_recipes_information(self):

        # User goes to the home page
        self.browser.get(self.live_server_url)

        self.wait_for_page("Welcome to ezcourses")

        # User clicks on the recipes button
        self.browser.find_element("id", "id_recipes_button").click()

        # User sees that he was redirected to the recipes page
        self.wait_for_page("Recipes")

        # User sees recipes table
        recipes_table = self.browser.find_element("id", "id_recipes_table")
        self.assertNotEqual(
            recipes_table.find_elements("css selector", "tr"),
            [],
            "The recipes table is empty",
        )

        # User sees tomato soup recipe
        self.assertIn("Tomato soup", recipes_table.text)

        # User check if the recipe contains the ingredients and their quantities
        tomato_soup_recipe_element = [
            recipe
            for recipe in recipes_table.find_elements("css selector", "tr")
            if "Tomato soup" in recipe.text
        ][0]

        self.assertIn("Tomato", tomato_soup_recipe_element.text)
        self.assertIn("3.00 Kg", tomato_soup_recipe_element.text)
