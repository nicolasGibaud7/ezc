from django.core.exceptions import ValidationError
from django.test import TestCase

from list_generation.models import (
    Category,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Shelf,
    ShoppingIngredient,
    ShoppingList,
    ShoppingListGeneration,
    Unit,
)


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


class RecipeIngredientsModelTest(TestCase):
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

    def test_saving_recipe_ingredients(self):
        RecipeIngredient.objects.create(
            ingredient=Ingredient.objects.first(),
            quantity=1,
        )
        self.assertEqual(RecipeIngredient.objects.count(), 1)

    def test_get_price(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            ingredient=Ingredient.objects.first(),
            quantity=2,
        )
        try:
            self.assertEqual(float(recipe_ingredient.get_price()), 2.60)
        except TypeError:
            raise TypeError("Ingredient price is not set")


class RecipeModelTest(TestCase):
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
            price=3.30,
        )
        Recipe.objects.create(name="Tomate soup")
        Recipe.objects.create(name="Onion soup")

    def test_saving_recipes(self):
        self.assertEqual(Recipe.objects.count(), 2)

    def test_retrieving_recipes(self):
        saved_recipes = Recipe.objects.all()

        first_saved_recipe = saved_recipes[0]
        second_saved_recipe = saved_recipes[1]
        self.assertEqual(first_saved_recipe.name, "Tomate soup")
        self.assertEqual(second_saved_recipe.name, "Onion soup")

    def test_adding_ingredients_to_recipe(self):
        tomato_recipe = Recipe.objects.first()
        tomato_recipe.add_ingredient(Ingredient.objects.first(), 1)
        self.assertEqual(tomato_recipe.ingredients.count(), 1)
        self.assertEqual(
            tomato_recipe.ingredients.first().ingredient.name, "Tomate"
        )

        onion_recipe = Recipe.objects.last()
        onion_recipe.add_ingredient(Ingredient.objects.last(), 2)
        self.assertEqual(onion_recipe.ingredients.count(), 1)
        self.assertEqual(
            onion_recipe.ingredients.first().ingredient.name, "Onion"
        )

    def test_ingredients_count(self):
        tomato_recipe = Recipe.objects.first()
        tomato_recipe.add_ingredient(Ingredient.objects.first(), 1)
        self.assertEqual(tomato_recipe.ingredients_count(), 1)

        tomato_recipe.add_ingredient(Ingredient.objects.last(), 1)
        self.assertEqual(tomato_recipe.ingredients_count(), 2)


class ShoppingListModelTest(TestCase):
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
        Recipe.objects.create(name="Tomate soup").add_ingredient(
            Ingredient.objects.first(), 1
        )
        ShoppingList.objects.create()

    def test_saving_shopping_list(self):
        self.assertEqual(ShoppingList.objects.count(), 1)

    def test_adding_recipe_to_shopping_list(self):
        ShoppingList.objects.first().add_recipe(Recipe.objects.first())
        self.assertEqual(ShoppingList.objects.first().recipes.count(), 1)
        self.assertEqual(
            ShoppingList.objects.first().recipes.first().name, "Tomate soup"
        )

    def test_adding_ingredients_to_shopping_list_generation(self):
        shopping_list = ShoppingList.objects.first()
        shopping_list._add_shopping_ingredient(Ingredient.objects.first(), 1)
        self.assertEqual(shopping_list.shopping_ingredients.count(), 1)

    def test_updating_ingredients_to_shopping_list_generation(self):
        shopping_list = ShoppingList.objects.first()
        shopping_list._add_shopping_ingredient(Ingredient.objects.first(), 1)
        self.assertEqual(
            shopping_list.shopping_ingredients.first().quantity,
            1,
        )

        shopping_list._update_shopping_ingredient(
            Ingredient.objects.first(), 1
        )
        self.assertEqual(
            shopping_list.shopping_ingredients.first().quantity,
            2,
        )

    def test_calculate_ingredients_quantities(self):
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
        ShoppingList.objects.first().add_recipe(Recipe.objects.first())
        ShoppingList.objects.first().add_recipe(Recipe.objects.last())

        shopping_list = ShoppingList.objects.first()
        shopping_list.calculate_ingredients_quantities()
        self.assertEqual(shopping_list.shopping_ingredients.count(), 2)
        self.assertEqual(
            shopping_list.shopping_ingredients.get(
                ingredient=Ingredient.objects.first()
            ).quantity,
            1,
        )
        self.assertEqual(
            shopping_list.shopping_ingredients.get(
                ingredient=Ingredient.objects.last()
            ).quantity,
            2,
        )

    def test_conversion_to_text_format(self):
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
        ShoppingList.objects.first().add_recipe(Recipe.objects.first())
        ShoppingList.objects.first().add_recipe(Recipe.objects.last())

        shopping_list = ShoppingList.objects.first()
        shopping_list.calculate_ingredients_quantities()
        shopping_list_text_representation = shopping_list.to_text()
        self.assertIn("Tomate - 1.00 Kg\n", shopping_list_text_representation)
        self.assertIn("Onion - 2.00 Kg", shopping_list_text_representation)


class ShoppingIngredientsModelTest(TestCase):
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

    def test_saving(self):
        ShoppingIngredient.objects.create(
            ingredient=Ingredient.objects.first(),
            quantity=1,
        )
        self.assertEqual(ShoppingIngredient.objects.count(), 1)

    def test_string_representation(self):
        shopping_ingredient = ShoppingIngredient.objects.create(
            ingredient=Ingredient.objects.first(),
            quantity=1,
        )
        self.assertEqual(
            str(shopping_ingredient),
            "Tomate - 1 Kg",
        )


class ShoppingListGenerationModelTest(TestCase):
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
            price=3.30,
        )
        Recipe.objects.create(name="Tomate soup").add_ingredient(
            Ingredient.objects.first(), 1
        )
        Recipe.objects.create(name="Onion soup").add_ingredient(
            Ingredient.objects.last(), 2
        )
        ShoppingList.objects.create().add_recipe(Recipe.objects.first())
        ShoppingList.objects.first().add_recipe(Recipe.objects.last())
        ShoppingListGeneration.objects.create(
            shopping_list=ShoppingList.objects.first(),
            mail="nicolas.gibaud7@gmail.com",
            sending_method="email",
            format_choice="pdf",
        )

    def test_creating_shopping_list_generation(self):
        self.assertEqual(ShoppingListGeneration.objects.count(), 1)

    def test_generate_shopping_list(self):
        shopping_list_generation = ShoppingListGeneration.objects.first()
        shopping_list_generation.generate_shopping_list()
        self.assertEqual(
            shopping_list_generation.shopping_list.shopping_ingredients.count(),
            2,
        )
        self.assertEqual(
            shopping_list_generation.shopping_list.shopping_ingredients.get(
                ingredient=Ingredient.objects.first()
            ).quantity,
            1,
        )
        self.assertEqual(
            shopping_list_generation.shopping_list.shopping_ingredients.get(
                ingredient=Ingredient.objects.last()
            ).quantity,
            2,
        )
