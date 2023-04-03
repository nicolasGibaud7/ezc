import os
import tempfile
from io import BytesIO

from django.core.files import File
from django.db import models

from ezc.mail_utility import get_mail_credentials, send_mail_with_attachment
from ezc.pdf_factory import PdfFactory

SENDING_METHODS = [("email", "email"), ("download", "download")]
FORMAT_CHOICES = [("txt", "txt"), ("pdf", "pdf")]


# Create your models here.
class Shelf(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(default="")


class Category(models.Model):
    name = models.CharField(max_length=100, default="")
    description = models.TextField(default="")


class Unit(models.Model):
    name = models.CharField(max_length=100, default="")
    abbreviation = models.CharField(max_length=10, default="")


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    def get_price(self):
        if not self.ingredient.price:
            return None
        return self.ingredient.price * self.quantity

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity}"


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(RecipeIngredient)

    def add_ingredient(self, ingredient, quantity):
        self.ingredients.add(
            RecipeIngredient.objects.create(
                ingredient=ingredient, quantity=quantity
            )
        )

    def ingredients_count(self):
        return self.ingredients.count()

    def __str__(self):
        return self.name


class ShoppingIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity} {self.ingredient.unit.abbreviation}"


class ShoppingList(models.Model):
    recipes = models.ManyToManyField(Recipe)
    shopping_ingredients = models.ManyToManyField(ShoppingIngredient)

    def add_recipe(self, recipe):
        self.recipes.add(recipe)

    def calculate_ingredients_quantities(self):
        for recipe in self.recipes.all():
            for recipe_ingredient in recipe.ingredients.all():
                ingredient = recipe_ingredient.ingredient
                quantity = recipe_ingredient.quantity
                if self.shopping_ingredients.filter(
                    ingredient=ingredient
                ).exists():
                    self._update_shopping_ingredient(ingredient, quantity)
                else:
                    self._add_shopping_ingredient(ingredient, quantity)

    def to_text(self) -> str:
        return "\n".join(
            [str(ingredient) for ingredient in self.shopping_ingredients.all()]
        )

    def to_pdf(self) -> bytes:

        with tempfile.TemporaryDirectory() as tmpdirname:
            pdf_factory = PdfFactory(
                os.path.join(tmpdirname, "temp_shopping_list.pdf")
            )
            ingredients = [
                (
                    ingredient.ingredient.name,
                    ingredient.ingredient.category.name,
                    ingredient.ingredient.shelf.name,
                    f"{ingredient.quantity} {ingredient.ingredient.unit.abbreviation}",
                    f"{ingredient.ingredient.price} €",
                )
                for ingredient in self.shopping_ingredients.all()
            ]
            pdf_factory.generate_shopping_list(ingredients)
            pdf_content = ""
            with open(pdf_factory.doc.filename, "rb") as pdf_file:
                pdf_content = pdf_file.read()

        return pdf_content

    def convert_to_text_format(self):
        text = ""
        for shopping_ingredient in self.shopping_ingredients.all():
            text += f"{shopping_ingredient.ingredient.name} - {shopping_ingredient.quantity} {shopping_ingredient.ingredient.unit.abbreviation}"

    def _add_shopping_ingredient(self, ingredient, quantity):
        shopping_ingredient = ShoppingIngredient.objects.create(
            ingredient=ingredient, quantity=quantity
        )
        self.shopping_ingredients.add(shopping_ingredient)

    def _update_shopping_ingredient(self, ingredient, quantity):
        shopping_ingredient = self.shopping_ingredients.get(
            ingredient=ingredient
        )
        shopping_ingredient.quantity += quantity
        shopping_ingredient.save()


class ShoppingListGeneration(models.Model):

    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    mail = models.EmailField()
    sending_method = models.CharField(
        choices=SENDING_METHODS, max_length=10, default="email"
    )
    format_choice = models.CharField(
        choices=FORMAT_CHOICES, max_length=3, default="txt"
    )
    pdf_file = None

    def generate_shopping_list(self):
        self.shopping_list.calculate_ingredients_quantities()

    def generate_pdf(self):
        shopping_list_pdf_content = self.shopping_list.to_pdf()
        self.pdf_file = File(BytesIO(shopping_list_pdf_content))

    def send_by_mail(self, receiver: str = "") -> bool:
        self.generate_pdf()

        if not receiver:
            receiver = self.mail

        sender, password = get_mail_credentials()
        body = "You can find your shopping list attached to this email."

        return send_mail_with_attachment(
            sender,
            password,
            receiver,
            "Shopping List",
            body,
            self.pdf_file,
        )
