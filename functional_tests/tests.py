import time

from django.test import LiveServerTestCase
from selenium import webdriver

from list_generation.models import Ingredient


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.live_server_url = "http://localhost:8000"

    def tearDown(self):
        self.browser.quit()

    def test_access_home_page_and_access_several_elements(self):
        # User goes to the home page
        self.browser.get(self.live_server_url)

        time.sleep(1)

        # User notices the page title and header mention ezcourses
        self.assertIn("Welcome to ezcourses", self.browser.title)

    # def test_select_recipe_and_see_it_in_the_selected_recipes_list(self):
    #     # User goes to the home page
    #     self.browser.get(self.live_server_url)

    #     time.sleep(1)

    #     # User clicks on the recipes button
    #     self.browser.find_element("id", "id_recipes_button").click()

    #     time.sleep(1)

    #     # User sees that he was redirected to the recipes page
    #     self.assertIn("Recipes", self.browser.title)

    #     self.fail("Finish the test!")

    #     # User selects the first recipe
    #     first_recipe = self.browser.find_element("id", "id_recipe_0")
    #     first_recipe_title = first_recipe.find_element("id", "id_recipe_title")

    #     first_recipe.find_element("id", "id_select_button").click()

    #     time.sleep(1)

    #     # User back to the home page
    #     self.browser.get("/")

    #     # User sees the recipe in the selected recipes list
    #     selected_recipe = self.browser.find_element(
    #         "id", "id_selected_recipe_0"
    #     )
    #     self.assertIsNotNone(
    #         selected_recipe
    #     )  # TODO Change this test because find_element will raise an exception if the element is not found

    #     # User check that is the same recipe that he selected
    #     self.assertEqual(
    #         first_recipe_title,
    #         selected_recipe.find_element("id", "id_recipe_title"),
    #     )

    #     self.fail("Finish the test!")

    def test_access_ingredients_page_and_see_ingredients_information(self):

        # User goes to the home page
        self.browser.get(self.live_server_url)

        time.sleep(1)

        # User clicks on the ingredients button
        self.browser.find_element("id", "id_ingredients_button").click()

        time.sleep(1)

        # User sees that he was redirected to the ingredients page
        self.assertIn("Ingredients", self.browser.title)

        # User sees ingredients table
        ingredients_table = self.browser.find_element(
            "id", "id_ingredients_table"
        )
        self.assertNotEqual(
            ingredients_table.find_elements("css selector", "tr"),
            [],
            "The ingredients table is empty",
        )

        # User clicks on the tomato ingredient
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

        self.fail("Finish the test!")

        # User sees that he was redirected to the ingredient details page
        self.assertIn(f"{tomato_ingredient_element.text}", self.browser.title)

        # User sees the ingredient details
        # TODO see How to test that there are ingredients details on the page

    def test_access_ingredients_details(self):

        # User goes to the ingredients page
        self.browser.get(self.live_server_url + "/ingredients/")

        # User clicks on the tomato ingredient
        self.fail("Finish the test!")

        # User sees that he was redirected to the ingredient details page

        # User check the ingredients details
