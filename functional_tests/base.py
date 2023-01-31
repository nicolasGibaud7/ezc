import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.live_server_url = "http://localhost:8000"

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, test_function):
        start_time = time.time()
        while True:
            try:
                return test_function()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_page(self, expected_title: str):
        self.wait_for(
            lambda: self.assertIn(expected_title, self.browser.title)
        )
