import time

from django.test import LiveServerTestCase
from selenium import webdriver


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.live_server_url = "http://localhost:8000"

    def tearDown(self):
        self.browser.quit()

    def test_access_home_page(self):
        # User goes to the home page
        self.browser.get(self.live_server_url)

        time.sleep(5)

        # User notices the page title and header mention ezcourses
        self.assertIn("Welcome to ezcourses", self.browser.title)

        self.fail("Finish the test!")
