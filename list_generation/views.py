from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from list_generation.models import Ingredient, Recipe, ShoppingList


# Create your views here.
def home_page(request):
    shopping_list = ShoppingList.objects.first()
    return render(request, "home.html", {"shopping_list": shopping_list})


def recipes_page(request):
    return render(request, "recipes.html", {"recipes": Recipe.objects.all()})


def ingredients_page(request):
    ingredients_ = Ingredient.objects.all()
    return render(request, "ingredients.html", {"ingredients": ingredients_})


def ingredient_details_page(request, ingredient_id):
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except Ingredient.DoesNotExist:
        return redirect("ingredients")

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


def select_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return HttpResponseNotFound("<h1>Recipe not found</h1>")
    try:
        ShoppingList.objects.first().add_recipe(recipe)
    except AttributeError:
        ShoppingList.objects.create().add_recipe(recipe)

    return redirect("recipes")


def shopping_list_generation(request):
    return render(
        request,
        "shopping_list_generation.html",
    )
