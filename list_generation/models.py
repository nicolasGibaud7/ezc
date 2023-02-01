from django.db import models


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


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    # ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name
