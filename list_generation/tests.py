from django.test import TestCase
from django.urls import resolve

from list_generation.views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>Welcome to ezcourses</title>", html)
        self.assertTrue(html.endswith("</html>"))
