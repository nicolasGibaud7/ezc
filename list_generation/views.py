from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from list_generation.forms import ShoppingListGenerationForm
from list_generation.models import (
    Ingredient,
    Recipe,
    ShoppingList,
    ShoppingListGeneration,
)

NO_RECIPES_SELECTED_ERRROR = "No recipes selected"

# Create your views here.
def home_page(request, errors=None):
    shopping_list = ShoppingList.objects.first()
    return render(
        request,
        "home.html",
        {"shopping_list": shopping_list, "errors": errors},
    )


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
    if request.method == "POST":
        form = ShoppingListGenerationForm(request.POST)

        if form.is_valid():
            shopping_list_generation = form.save(commit=False)
            shopping_list_generation.shopping_list = (
                ShoppingList.objects.first()
            )
            shopping_list_generation.generate_shopping_list()
            shopping_list_generation.save()
            shopping_list_generation.send_by_mail()

            return redirect("home")
        else:
            return render(
                request,
                "shopping_list_generation.html",
                {
                    "form": form,
                    "shopping_list": ShoppingList.objects.first(),
                    "errors": form.errors,
                },
            )

    shopping_list = ShoppingList.objects.first()
    if not shopping_list:
        shopping_list = ShoppingList.objects.create()

    if not shopping_list.recipes.all():
        return render(request, "home.html", {"error": "No recipes selected"})

    form = ShoppingListGenerationForm()
    return render(
        request,
        "shopping_list_generation.html",
        {"form": form, "shopping_list": shopping_list},
    )
