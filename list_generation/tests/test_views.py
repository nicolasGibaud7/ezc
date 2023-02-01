from unittest import skip

from django.test import TestCase
from django.urls import resolve

from list_generation.models import Category, Ingredient, Recipe, Shelf, Unit
from list_generation.views import (
    home_page,
    ingredient_details_page,
    ingredients_page,
    recipe_details_page,
    recipes_page,
)


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

    def test_recipes_page_returns_recipes_list(self):
        recipes = ["Tomato soup", "Onion soup"]

        for recipe in recipes:
            Recipe.objects.create(name=recipe)

        response = self.client.get("/recipes/")
        self.assertEqual(
            list(response.context["recipes"]), list(Recipe.objects.all())
        )

    def test_display_all_recipes(self):
        recipes = ["Tomato soup", "Onion soup"]

        for recipe in recipes:
            Recipe.objects.create(name=recipe)

        response = self.client.get("/recipes/").content.decode()
        for recipe in recipes:
            self.assertIn(recipe, response)

    def test_display_ingredients_of_a_recipe(self):

        Category.objects.create(name="Market")
        Shelf.objects.create(name="Fruits and vegetables")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Ingredient.objects.create(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.30,
        )

        tomato_soup = Recipe.objects.create(name="Tomato soup")
        tomato_soup.add_ingredient(Ingredient.objects.first(), 1)

        response = self.client.get("/recipes/").content.decode()
        self.assertIn("Tomato", response)
        self.assertIn("1.00 Kg", response)

    def test_recipe_button_presence(self):
        """
        Check recipe detail button presence.
        """
        recipes = ["Tomato soup", "Onion soup"]

        for recipe in recipes:
            Recipe.objects.create(name=recipe)

        response = self.client.get("/recipes/").content.decode()
        for recipe in recipes:
            self.assertIn(
                f'<a href="/recipes/{Recipe.objects.get(name=recipe).id}/"',
                response,
            )


class RecipeDetailsPageTest(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name="Market")
        Shelf.objects.create(name="Fruits and vegetables")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Ingredient.objects.create(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.30,
        )
        Recipe.objects.create(name="Tomato soup")

    def test_recipe_details_url_resolves_to_recipe_details_page_view(
        self,
    ):
        found = resolve("/recipes/1/")
        self.assertEqual(found.func, recipe_details_page)

    def test_recipe_details_page_returns_correct_html(self):
        response = self.client.get("/recipes/1/")
        self.assertTemplateUsed(response, "recipe_details.html")

    def test_recipe_details_page_returns_recipe(self):
        recipe = Recipe.objects.create(name="Tomato soup")

        response = self.client.get(f"/recipes/{recipe.id}/")
        self.assertEqual(response.context["recipe"], recipe)

    def test_display_ingredients_of_a_recipe(self):
        tomato_soup = Recipe.objects.first()
        tomato_soup.add_ingredient(Ingredient.objects.first(), 1)

        response = self.client.get(
            f"/recipes/{tomato_soup.id}/"
        ).content.decode()
        self.assertIn("Tomato", response)
        self.assertIn("1.00", response)
        self.assertIn("Kilogram (Kg)", response)
        self.assertIn("1.30", response)

    def test_display_ingredient_price(self):
        tomato_soup = Recipe.objects.first()
        tomato_soup.add_ingredient(Ingredient.objects.first(), 2)

        response = self.client.get(
            f"/recipes/{tomato_soup.id}/"
        ).content.decode()
        self.assertIn("2.60", response)


class IngredientsPageTest(TestCase):
    def setUp(self):
        Shelf.objects.create(name="Fruits and vegetables")
        Category.objects.create(name="Market")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")

    def test_ingredients_url_resolves_to_ingredients_page_view(self):
        found = resolve("/ingredients/")
        self.assertEqual(found.func, ingredients_page)

    def test_ingredients_page_returns_correct_html(self):
        response = self.client.get("/ingredients/")

        self.assertTemplateUsed(response, "ingredients.html")

    def test_display_all_ingredients(self):
        ingredients_info = [
            {
                "name": "Tomate",
                "shelf": Shelf.objects.first(),
                "category": Category.objects.first(),
                "unit": Unit.objects.first(),
                "price": 1.3,
            },
            {
                "name": "Oignon",
                "shelf": Shelf.objects.first(),
                "category": Category.objects.first(),
                "unit": Unit.objects.first(),
                "price": 1.3,
            },
            {
                "name": "Ail",
                "shelf": Shelf.objects.first(),
                "category": Category.objects.first(),
                "unit": Unit.objects.first(),
                "price": 1.3,
            },
            {
                "name": "Piment",
                "shelf": Shelf.objects.first(),
                "category": Category.objects.first(),
                "unit": Unit.objects.first(),
                "price": 1.3,
            },
        ]
        for ingredient_info in ingredients_info:
            Ingredient.objects.create(
                name=ingredient_info["name"],
                shelf=ingredient_info["shelf"],
                category=ingredient_info["category"],
                unit=ingredient_info["unit"],
                price=ingredient_info["price"],
            )

        response = self.client.get("/ingredients/").content.decode()
        for ingredient_info in ingredients_info:
            self.assertIn(ingredient_info["name"], response)
            self.assertIn(ingredient_info["shelf"].name, response)
            self.assertIn(ingredient_info["category"].name, response)
            self.assertIn(ingredient_info["unit"].name, response)
            self.assertIn(str(ingredient_info["price"]), response)

    def test_ingredient_button_presence(self):
        """
        Check ingredient detail button presence.
        """
        Ingredient.objects.create(
            name="Tomate",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.3,
        )
        response = self.client.get("/ingredients/").content.decode()

        self.assertIn(
            f'<button id="id_details_button_{Ingredient.objects.first().id}">',
            response,
        )

    def test_ingredient_button_redirect_to_ingredient_details_page(self):
        """
        Check if the link associated to the ingredient detail button is correct
        """
        Ingredient.objects.create(
            name="Tomate",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.3,
        )
        response = self.client.get("/ingredients/").content.decode()

        self.assertIn(
            f'<a href="/ingredients/{Ingredient.objects.first().id}/"',
            response,
        )


class IngredientDetailPageTest(TestCase):
    def setUp(self):
        Shelf.objects.create(name="Fruits and vegetables")
        Category.objects.create(name="Market")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Ingredient.objects.create(
            name="Tomate",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.3,
        )

    def test_ingredients_detail_url_resolves_to_ingredients_detail_page_view(
        self,
    ):
        found = resolve(f"/ingredients/{Ingredient.objects.first().id}/")
        self.assertEqual(found.func, ingredient_details_page)

    def test_ingredients_detail_page_returns_correct_html(self):
        response = self.client.get(
            f"/ingredients/{Ingredient.objects.first().id}/"
        )

        self.assertTemplateUsed(response, "ingredient_details.html")

    def test_retrieving_ingredient_object(self):
        """
        Get the ingredient object used by the view to display the ingredient.
        We could get the information by using context["ingredient"]
        """
        ingredient = Ingredient.objects.first()
        response = self.client.get(f"/ingredients/{ingredient.id}/").context[
            "ingredient"
        ]
        self.assertEqual(response, ingredient)

    def test_retrieving_ingredient_information(self):
        ingredient = Ingredient.objects.first()
        response = self.client.get(
            f"/ingredients/{ingredient.id}/"
        ).content.decode()
        self.assertIn(ingredient.name, response)
        self.assertIn(ingredient.shelf.name, response)
        self.assertIn(ingredient.category.name, response)
        self.assertIn(ingredient.unit.name, response)
        self.assertIn(str(ingredient.price), response)

    def test_unit_special_display(self):
        ingredient = Ingredient.objects.first()
        response = self.client.get(
            f"/ingredients/{ingredient.id}/"
        ).content.decode()
        self.assertIn(
            f"{ingredient.unit.name} ({ingredient.unit.abbreviation})",
            response,
        )

    def test_access_to_an_unknown_ingredient_details(self):
        response = self.client.get("/ingredients/999/")
        self.assertInHTML(
            "<title>Ingredients</title>", response.content.decode()
        )
