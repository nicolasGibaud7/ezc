from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest


class ShoppingListGeneration(FunctionalTest):
    def test_select_recipes_and_see_them_on_home_page(self):

        # User goes to the home page
        self.browser.get(self.live_server_url)

        # User sees empty selected recipes table
        try:
            selected_recipes_table = self.browser.find_element(
                "id", "id_selected_recipes_table"
            )
        except NoSuchElementException:
            raise AssertionError("No selected recipes table found.")

        self.assertEqual(
            selected_recipes_table.find_elements("css selector", "tr"),
            [],
            "The selected recipes table must be empty",
        )

        # User goes to the recipes page
        self.browser.find_element("id", "id_recipes_button").click()
        self.wait_for_page("Recipes")

        # User see not empty recipes table
        recipes_table = self.browser.find_element("id", "id_recipes_table")
        self.assertNotEqual(
            recipes_table.find_elements("css selector", "tr"),
            [],
            "The recipes table is empty",
        )

        # User selects the tomato soup recipe
        self.browser.find_element("id", "id_select_button_1").click()

        # User go back to the home page
        self.browser.get(self.live_server_url)

        # User sees the tomato soup recipe on the selected recipes table
        selected_recipes_table = self.browser.find_element(
            "id", "id_selected_recipes_table"
        )
        self.assertNotEqual(
            selected_recipes_table.find_elements("css selector", "tr"),
            [],
            "The recipes table is empty",
        )
        self.assertIn("Tomato soup", selected_recipes_table.text)
