import time

from django.test import LiveServerTestCase
from selenium import webdriver


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

    def test_select_recipe_and_see_it_in_the_selected_recipes_list(self):
        # User goes to the home page
        self.browser.get(self.live_server_url)

        time.sleep(1)

        # User clicks on the recipes button
        self.browser.find_element("id", "id_recipes_button").click()

        time.sleep(1)

        # User sees that he was redirected to the recipes page
        self.assertIn("Recipes", self.browser.title)

        self.fail("Finish the test!")

        # User selects the first recipe
        first_recipe = self.browser.find_element("id", "id_recipe_0")
        first_recipe_title = first_recipe.find_element("id", "id_recipe_title")

        first_recipe.find_element("id", "id_select_button").click()

        time.sleep(1)

        # User back to the home page
        self.browser.get("/")

        # User sees the recipe in the selected recipes list
        selected_recipe = self.browser.find_element(
            "id", "id_selected_recipe_0"
        )
        self.assertIsNotNone(
            selected_recipe
        )  # TODO Change this test because find_element will raise an exception if the element is not found

        # User check that is the same recipe that he selected
        self.assertEqual(
            first_recipe_title,
            selected_recipe.find_element("id", "id_recipe_title"),
        )

        self.fail("Finish the test!")
