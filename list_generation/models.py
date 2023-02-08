from django.db import models

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


class ShoppingList(models.Model):
    recipes = models.ManyToManyField(Recipe)

    def add_recipe(self, recipe):
        self.recipes.add(recipe)


class ShoppingListGeneration(models.Model):

    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    mail = models.EmailField()
    sending_method = models.CharField(
        choices=SENDING_METHODS, max_length=10, default="email"
    )
    format_choice = models.CharField(
        choices=FORMAT_CHOICES, max_length=3, default="txt"
    )
