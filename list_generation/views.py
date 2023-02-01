from django.http import HttpResponseNotFound
from django.shortcuts import render

from list_generation.models import Ingredient, Recipe


# Create your views here.
def home_page(request):
    return render(request, "home.html")


def recipes_page(request):
    return render(request, "recipes.html", {"recipes": Recipe.objects.all()})


def ingredients_page(request):
    ingredients_ = Ingredient.objects.all()
    return render(request, "ingredients.html", {"ingredients": ingredients_})


def ingredient_details_page(request, ingredient_id):
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except Ingredient.DoesNotExist:
        return ingredients_page(request)

    return render(
        request, "ingredient_details.html", {"ingredient": ingredient}
    )


def recipe_details_page(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return HttpResponseNotFound("<h1>Recipe not found</h1>")
    return render(
        request,
        "recipe_details.html",
        {"recipe": recipe},
    )
