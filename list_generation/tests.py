from django.test import TestCase
from django.urls import resolve

from list_generation.models import Ingredient
from list_generation.views import home_page, ingredients_page, recipes_page


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


class IngredientsPageTest(TestCase):
    def test_ingredients_url_resolves_to_ingredients_page_view(self):
        found = resolve("/ingredients/")
        self.assertEqual(found.func, ingredients_page)

    def test_ingredients_page_returns_correct_html(self):
        response = self.client.get("/ingredients/")

        self.assertTemplateUsed(response, "ingredients.html")

    def test_ingredients_are_displayed(self):
        ingredients = ["Tomate", "Oignon", "Ail", "Piment"]
        for ingredient in ingredients:
            Ingredient(name=ingredient).save()

        response = self.client.get("/ingredients/")
        for ingredient in ingredients:
            self.assertIn(ingredient, response.content.decode())


class IngredientsModelTest(TestCase):
    def test_saving_and_retrieving_ingredients(self):
        Ingredient(name="Tomate").save()
        Ingredient(name="Oignon").save()

        saved_ingredients = Ingredient.objects.all()
        self.assertEqual(saved_ingredients.count(), 2)

        first_saved_ingredient = saved_ingredients[0]
        second_saved_ingredient = saved_ingredients[1]
        self.assertEqual(first_saved_ingredient.name, "Tomate")
        self.assertEqual(second_saved_ingredient.name, "Oignon")
