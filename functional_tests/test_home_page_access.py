from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_simple_home_page_access(self):
        # User goes to the home page
        self.browser.get(self.live_server_url)

        # User notices the page title and header mention ezcourses
        self.wait_for_page("Welcome to ezcourses")
