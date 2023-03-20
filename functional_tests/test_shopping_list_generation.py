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
            selected_recipes_table.find_elements("css selector", "div"),
            [],
            "The selected recipes table must be empty",
        )

        # User goes to the recipes page
        self.browser.find_element("id", "id_recipes_link").click()
        self.wait_for_page("Recipes")

        # User see not empty recipes table
        recipes_table = self.browser.find_element("id", "id_recipes_table")
        self.assertNotEqual(
            recipes_table.find_elements("css selector", "div"),
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
            selected_recipes_table.find_elements("css selector", "div"),
            [],
            "The selected recipes table is empty",
        )
        self.assertIn("Tomato soup", selected_recipes_table.text)

    def test_cant_access_shopping_list_generation_page_if_no_recipes_selected(
        self,
    ):
        # User goes to the shopping list generation page
        self.browser.get(self.live_server_url + "/shopping_list_generation/")

        # User sees that he was redirected to the home page
        self.wait_for_page("Welcome to ezcourses")

        # User sees the error message
        error_message = self.browser.find_element("id", "id_error_message")
        self.assertIn("No recipes selected", error_message.text)

    def test_access_shopping_list_generation_page(self):
        # User goes to the recipes page
        self.browser.get(self.live_server_url + "/recipes/")
        self.wait_for_page("Recipes")

        # User select tomato oup recipe
        self.browser.find_element("id", "id_select_button_1").click()

        # User go back to the home page
        self.browser.get(self.live_server_url)
        self.wait_for_page("Welcome to ezcourses")

        # User clicks on the shopping list generation button
        self.browser.find_element(
            "id", "id_shopping_list_generation_button"
        ).click()

        # User sees that he was redirected to the shopping list generation page
        self.wait_for_page("Shopping list generation")

        # User sees the form fields
        self.browser.find_element("id", "id_form")

        # User keeps the default sending method "email"

        # User keeps the default format "txt"

        # User fill the email form field with nicolas.gibaud7@gmail.com
        self.browser.find_element("id", "id_email").send_keys(
            "nicolas.gibaud7@gmail.com"
        )

        # User clicks on the generation button
        self.browser.find_element("id", "id_generation_button").click()

        # User sees that he was redirected to the home page
        self.wait_for_page("Welcome to ezcourses")

        # User checks he has received the mail with the shopping list
        self.fail("Finish the test!")
