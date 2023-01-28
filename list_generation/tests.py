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
        ingredients = ["Tomate", "Oignon", "Ail", "Piment"]
        shelf = Shelf.objects.first()
        category = Category.objects.first()
        unit = Unit.objects.first()
        for ingredient in ingredients:
            Ingredient(
                name=ingredient,
                shelf=shelf,
                category=category,
                unit=unit,
                price=1.3,
            ).save()

        response = self.client.get("/ingredients/")
        for ingredient in ingredients:
            self.assertIn(ingredient, response.content.decode())
            self.assertIn("Fruits and vegetables", response.content.decode())
            self.assertIn("Market", response.content.decode())
            self.assertIn("Kilogram (Kg)", response.content.decode())
            self.assertIn("1.30 €", response.content.decode())


class ShelfModelTest(TestCase):
    def test_saving_and_retrieving_shelfs(self):
        Shelf(name="Fruits and vegetables").save()
        Shelf(name="Dairy products").save()

        saved_shelfs = Shelf.objects.all()
        self.assertEqual(saved_shelfs.count(), 2)

        first_saved_shelf = saved_shelfs[0]
        second_saved_shelf = saved_shelfs[1]
        self.assertEqual(first_saved_shelf.name, "Fruits and vegetables")
        self.assertEqual(second_saved_shelf.name, "Dairy products")


class UnitModelTest(TestCase):
    def test_saving_and_retrieving_units(self):
        Unit(name="Kilogram", abbreviation="Kg").save()
        Unit(name="Gram", abbreviation="g").save()

        saved_units = Unit.objects.all()
        self.assertEqual(saved_units.count(), 2)

        first_saved_unit = saved_units[0]
        second_saved_unit = saved_units[1]
        self.assertEqual(first_saved_unit.name, "Kilogram")
        self.assertEqual(first_saved_unit.abbreviation, "Kg")
        self.assertEqual(second_saved_unit.name, "Gram")
        self.assertEqual(second_saved_unit.abbreviation, "g")


class CategoryModelTest(TestCase):
    def test_saving_and_retrieving_categories(self):
        Category(name="Market").save()
        Category(name="Frozen food").save()

        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 2)

        first_saved_category = saved_categories[0]
        second_saved_category = saved_categories[1]
        self.assertEqual(first_saved_category.name, "Market")
        self.assertEqual(second_saved_category.name, "Frozen food")


class IngredientsModelTest(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name="Market")
        Shelf.objects.create(name="Fruits and vegetables")
        Unit.objects.create(name="Kilogram", abbreviation="Kg")

    def test_saving_and_retrieving_ingredients(self):

        Ingredient(
            name="Tomate",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
        ).save()
        Ingredient(
            name="Oignon",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
        ).save()

        saved_ingredients = Ingredient.objects.all()
        self.assertEqual(saved_ingredients.count(), 2)

        first_saved_ingredient = saved_ingredients[0]
        second_saved_ingredient = saved_ingredients[1]
        self.assertEqual(first_saved_ingredient.name, "Tomate")
        self.assertEqual(second_saved_ingredient.name, "Oignon")

    def test_ingredients_have_shelf_attributes(self):
        Ingredient(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
        ).save()

        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(
            first_saved_ingredient.shelf.name, "Fruits and vegetables"
        )

    def test_ingredients_have_category_attributes(self):
        Ingredient(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
        ).save()

        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(first_saved_ingredient.category.name, "Market")

    def test_ingredient_have_unit_attributes(self):
        Ingredient(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
        ).save()

        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(first_saved_ingredient.unit.name, "Kilogram")

    def test_ingredient_have_price_attributes(self):
        Ingredient(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
            price=1.5,
        ).save()
        Ingredient(
            name="Tomato",
            shelf=Shelf.objects.first(),
            category=Category.objects.first(),
            unit=Unit.objects.first(),
        ).save()

        saved_ingredients = Ingredient.objects.all()

        first_saved_ingredient = saved_ingredients[0]
        self.assertEqual(first_saved_ingredient.price, 1.5)

        second_saved_ingredient = saved_ingredients[1]
        self.assertIsNone(second_saved_ingredient.price)
