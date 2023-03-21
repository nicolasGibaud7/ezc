from unittest import skip

from django.test import TestCase
from django.urls import resolve

from list_generation.forms import ShoppingListGenerationForm
from list_generation.models import (
    Category,
    Ingredient,
    Recipe,
    Shelf,
    ShoppingList,
    ShoppingListGeneration,
    Unit,
)
from list_generation.views import (
    home_page,
    ingredient_details_page,
    ingredients_page,
    recipe_details_page,
    recipes_page,
    select_recipe,
    shopping_list_generation,
)


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_get_shopping_list_element_from_context(self):
        ShoppingList.objects.create()

        response = self.client.get("/")
        self.assertEqual(
            response.context["shopping_list"], ShoppingList.objects.first()
        )

    def test_access_no_existing_shopping_list_and_get_none(self):
        response = self.client.get("/")
        self.assertEqual(response.context["shopping_list"], None)

    def test_display_selected_recipes(self):
        recipes = ["Tomato soup", "Onion soup"]

        for recipe in recipes:
            Recipe.objects.create(name=recipe)
        ShoppingList.objects.create()
        ShoppingList.objects.first().add_recipe(Recipe.objects.first())
        ShoppingList.objects.first().add_recipe(Recipe.objects.last())

        response = self.client.get("/").content.decode()

        for recipe in recipes:
            self.assertIn(recipe, response)

    def test_shopping_list_generation_button_redirects_to_shopping_list_page(
        self,
    ):
        Shelf.objects.create(name="Fruits and vegetables")
        Category.objects.create(name="Market")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Ingredient.objects.create(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.3,
        )
        Recipe.objects.create(name="Tomato soup").add_ingredient(
            Ingredient.objects.first(), 1
        )
        ShoppingList.objects.create().add_recipe(Recipe.objects.first())

        response = self.client.get(
            "/shopping_list_generation/",
        )

        self.assertIn("Shopping list generation", response.content.decode())


class RecipesPageTest(TestCase):
    def test_use_recipe_template(self):
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

    def test_display_ingredients_count_of_a_recipe(self):

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
        self.assertIn("1 ingredients", response)

    def test_recipe_detail_button_presence(self):
        recipes = ["Tomato soup", "Onion soup"]

        for recipe in recipes:
            Recipe.objects.create(name=recipe)

        response = self.client.get("/recipes/").content.decode()
        for recipe in recipes:
            self.assertIn(
                f'href="/recipes/{Recipe.objects.get(name=recipe).id}/"',
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

    def test_uses_recipe_detail_templates(self):
        recipe_ = Recipe.objects.first()
        response = self.client.get(f"/recipes/{recipe_.id}/")
        self.assertTemplateUsed(response, "recipe_details.html")

    def test_returns_404_if_recipe_does_not_exist(self):
        response = self.client.get("/recipes/999/")
        self.assertEqual(response.status_code, 404)

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
        self.assertIn("1.00Kg", response)


class IngredientsPageTest(TestCase):
    def setUp(self):
        Shelf.objects.create(name="Fruits and vegetables")
        Category.objects.create(name="Market")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")

    def test_uses_ingredients_tempplates(self):
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

    def test_uses_ingredient_detail_template(self):
        response = self.client.get(
            f"/ingredients/{Ingredient.objects.first().id}/"
        )
        self.assertTemplateUsed(response, "ingredient_details.html")

    def test_retrieving_ingredient_object(self):
        ingredient = Ingredient.objects.first()
        response = self.client.get(f"/ingredients/{ingredient.id}/").context[
            "ingredient"
        ]
        self.assertEqual(response, ingredient)

    def test_unit_special_display(self):
        ingredient = Ingredient.objects.first()
        response = self.client.get(
            f"/ingredients/{ingredient.id}/"
        ).content.decode()
        self.assertIn(
            f"{ingredient.unit.name} ({ingredient.unit.abbreviation})",
            response,
        )

    def test_return_404_when_trying_to_access_to_an_unknown_ingredient_details(
        self,
    ):
        response = self.client.get("/ingredients/999/")
        self.assertRedirects(response, "/ingredients/")


class AddRecipePageTest(TestCase):
    def setUp(self):
        Shelf.objects.create(name="Fruits and vegetables")
        Category.objects.create(name="Market")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Ingredient.objects.create(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.3,
        )
        Recipe.objects.create(name="Tomato soup").add_ingredient(
            Ingredient.objects.first(), 1
        )
        ShoppingList.objects.create()

    def test_add_recipe_url_resolves_to_add_recipe_page_view(self):
        found = resolve("/recipes/1/select/")
        self.assertEqual(found.func, select_recipe)

    def test_add_recipe_to_the_shopping_list(self):
        self.client.get("/recipes/1/select/")
        self.assertEqual(ShoppingList.objects.first().recipes.count(), 1)

    def test_redirect_to_recipes_page(self):
        response = self.client.get("/recipes/1/select/")
        self.assertRedirects(response, "/recipes/")

    def test_returns_404_if_recipe_does_not_exist(self):
        response = self.client.get("/recipes/999/select/")
        self.assertEqual(response.status_code, 404)

    def test_create_shopping_list_if_it_does_not_exist(self):
        ShoppingList.objects.all().delete()
        self.client.get("/recipes/1/select/")
        self.assertEqual(ShoppingList.objects.count(), 1)


class ShoppingListGenerationPageTest(TestCase):
    def setUp(self):
        Shelf.objects.create(name="Fruits and vegetables")
        Category.objects.create(name="Market")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Ingredient.objects.create(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.3,
        )
        Recipe.objects.create(name="Tomato soup").add_ingredient(
            Ingredient.objects.first(), 1
        )
        ShoppingList.objects.create().add_recipe(Recipe.objects.first())

    def test_url_resolves_to_shopping_list_generation_page_view(
        self,
    ):
        found = resolve("/shopping_list_generation/")
        self.assertEqual(found.func, shopping_list_generation)

    def test_page_returns_correct_html(self):
        response = self.client.get(
            "/shopping_list_generation/",
        )
        self.assertTemplateUsed(response, "shopping_list_generation.html")

    def test_shopping_list_generation_page_contains_a_form(self):
        response = self.client.get(
            "/shopping_list_generation/",
        )
        self.assertIsInstance(
            response.context["form"], ShoppingListGenerationForm
        )

    def test_display_a_form_with_a_mail_field(self):
        response = self.client.get(
            "/shopping_list_generation/",
        )
        self.assertIn("Mail", response.content.decode())

    def test_no_crash_when_no_shopping_list_are_created(self):
        ShoppingList.objects.all().delete()
        response = self.client.get(
            "/shopping_list_generation/",
        )
        self.assertIn("Welcome to ezcourses", response.content.decode())

    def test_redirect_to_home_page_if_no_recipes_are_selected_and_display_error_message(
        self,
    ):
        ShoppingList.objects.first().recipes.clear()
        response = self.client.get(
            "/shopping_list_generation/",
        )
        self.assertIn("Welcome to ezcourses", response.content.decode())
        self.assertIn("No recipes selected", response.content.decode())

    def test_display_generation_button(self):
        response = self.client.get(
            "/shopping_list_generation/",
        )
        self.assertIn(
            '<button id="id_generation_button" type="submit"',
            response.content.decode(),
        )

    def test_receive_POST_request_information(self):
        self.assertIsNone(ShoppingListGeneration.objects.first())
        response = self.client.post(
            "/shopping_list_generation/",
            {
                "mail": "nicolas.gibaud7@gmail.com",
                "format_choice": "pdf",
                "sending_method": "email",
            },
        )
        self.assertIsNotNone(ShoppingListGeneration.objects.first())

    def test_display_error_message_if_mail_is_incorrect(self):
        response = self.client.post(
            "/shopping_list_generation/",
            {
                "mail": "nicolas",
                "format_choice": "pdf",
                "sending_method": "email",
            },
        )
        self.assertIn(
            "Please enter a valid email address", response.content.decode()
        )

    def test_retrieve_shopping_list_ingredients_quantities(self):
        Ingredient.objects.create(
            name="Onion",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=3.30,
        )
        Recipe.objects.create(name="Onion soup").add_ingredient(
            Ingredient.objects.last(), 2
        )
        ShoppingList.objects.first().add_recipe(Recipe.objects.last())

        response = self.client.post(
            "/shopping_list_generation/",
            {
                "mail": "nicolas.gibaud7@gmail.co",
                "format_choice": "pdf",
                "sending_method": "email",
            },
        )
        self.assertEqual(
            ShoppingList.objects.first().shopping_ingredients.count(),
            2,
        )
        self.assertEqual(
            ShoppingList.objects.first().shopping_ingredients.first().quantity,
            1,
        )
        self.assertEqual(
            ShoppingList.objects.first().shopping_ingredients.last().quantity,
            2,
        )
