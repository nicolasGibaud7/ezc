from django.test import TestCase
from django.urls import resolve

from list_generation.views import home_page, recipes_page


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")

        self.assertTemplateUsed(response, "home.html")


class RecipesPageTest(TestCase):
    def test_recipes_url_resolves_to_recipes_page_view(self):
        found = resolve("/recipes/")
        self.assertEqual(found.func, recipes_page)

    def test_recipes_page_returns_correct_html(self):
        response = self.client.get("/recipes/")

        self.assertTemplateUsed(response, "recipes.html")

    def test_recipes_list_appears(self):
        pass
