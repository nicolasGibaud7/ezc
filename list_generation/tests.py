from django.test import TestCase
from django.urls import resolve

from list_generation.models import Category, Ingredient, Shelf, Unit
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

    def test_ingredients_are_displayed(self):
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


class ShelfModelTest(TestCase):
    def setUp(self):
        Shelf.objects.create(name="Fruits and vegetables")
        Shelf.objects.create(name="Dairy products")

    def test_saving_shelfs(self):
        self.assertEqual(Shelf.objects.count(), 2)

    def test_retrieving_shelfs(self):
        saved_shelfs = Shelf.objects.all()

        first_saved_shelf = saved_shelfs[0]
        second_saved_shelf = saved_shelfs[1]
        self.assertEqual(first_saved_shelf.name, "Fruits and vegetables")
        self.assertEqual(second_saved_shelf.name, "Dairy products")


class UnitModelTest(TestCase):
    def setUp(self) -> None:
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Unit.objects.create(name="Gram", abbreviation="g")

    def test_saving_units(self):
        self.assertEqual(Unit.objects.count(), 2)

    def test_retrieving_units(self):
        saved_units = Unit.objects.all()

        first_saved_unit = saved_units[0]
        second_saved_unit = saved_units[1]
        self.assertEqual(first_saved_unit.name, "Kilogram")
        self.assertEqual(first_saved_unit.abbreviation, "Kg")
        self.assertEqual(second_saved_unit.name, "Gram")
        self.assertEqual(second_saved_unit.abbreviation, "g")


class CategoryModelTest(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name="Market")
        Category.objects.create(name="Frozen food")

    def test_saving_categories(self):
        self.assertEqual(Category.objects.count(), 2)

    def test_retrieving_categories(self):
        saved_categories = Category.objects.all()

        first_saved_category = saved_categories[0]
        second_saved_category = saved_categories[1]
        self.assertEqual(first_saved_category.name, "Market")
        self.assertEqual(second_saved_category.name, "Frozen food")


class IngredientsModelTest(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name="Market")
        Shelf.objects.create(name="Fruits and vegetables")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")
        Ingredient.objects.create(
            name="Tomate",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.30,
        )
        Ingredient.objects.create(
            name="Onion",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
        )

    def test_saving_ingredients(self):
        self.assertEqual(Ingredient.objects.count(), 2)

    def test_retrieving_ingredients(self):
        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        second_saved_ingredient = saved_ingredients[1]
        self.assertEqual(first_saved_ingredient.name, "Tomate")
        self.assertEqual(second_saved_ingredient.name, "Onion")

    def test_ingredients_have_shelf_attributes(self):
        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(
            first_saved_ingredient.shelf.name, "Fruits and vegetables"
        )

    def test_ingredients_have_category_attributes(self):
        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(first_saved_ingredient.category.name, "Market")

    def test_ingredient_have_unit_attributes(self):
        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(first_saved_ingredient.unit.name, "Kilogram")

    def test_ingredient_have_price_attributes(self):
        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(str(first_saved_ingredient.price), "1.30")

        second_saved_ingredient = saved_ingredients[1]
        self.assertIsNone(second_saved_ingredient.price)
