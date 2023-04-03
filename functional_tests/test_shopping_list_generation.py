import os
import tempfile
import time

from PyPDF2 import PdfReader
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from ezc.mail_utility import get_last_mail_content, get_mail_credentials

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

    def test_get_pdf_shopping_list_by_email(self):
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

        # User change the sending method to "email"
        sending_method_select = Select(
            self.browser.find_element("id", "id_sending_method")
        )
        sending_method_select.select_by_value("email")

        # User change the format to "pdf"
        format_select = Select(
            self.browser.find_element("id", "id_format_choice")
        )
        format_select.select_by_value("pdf")

        # User fill the email form field with
        self.browser.find_element("id", "id_email").send_keys(
            "ez.courses.dev@gmail.com"
        )
        time.sleep(1)

        # User click on generate button
        self.browser.find_element("id", "id_generation_button").click()
        time.sleep(5)

        # User checks that he received the mail with the shopping list

        #   Credentials
        username, password = get_mail_credentials()

        last_mail_content = get_last_mail_content(username, password)

        #   Check that the subject is correct
        self.assertEqual("Shopping List", last_mail_content["subject"])

        #  Check that the body is correct
        self.assertIn(
            "You can find your shopping list attached to this email.",
            last_mail_content["body"],
        )

        #  Check that the attachment is correct
        try:
            last_mail_content["attachment"]
        except KeyError:
            self.fail("No attachments found in the email.")

        self.assertEqual(
            last_mail_content["attachment"]["filename"], "shopping_list.pdf"
        )
        # Create temporary file, write the attachment and read it with PdfReader to check the content
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(
                tmp_dir, last_mail_content["attachment"]["filename"]
            )
            with open(tmp_file, "wb") as f:
                f.write(last_mail_content["attachment"]["content"])
            pdf = PdfReader(tmp_file)
            self.assertIn(
                "Tomato",
                pdf.pages[0].extract_text(),
            )
            self.assertNotIn("Banana", pdf.pages[0].extract_text())

    def test_access_shopping_list_generation_page(self):
        # User goes to the recipes page
        self.browser.get(self.live_server_url + "/recipes/")
        self.wait_for_page("Recipes")

        # User select tomato soup recipe
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
