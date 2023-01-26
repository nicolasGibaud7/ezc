from django.http import HttpResponse
from django.shortcuts import render

from list_generation.models import Ingredient


# Create your views here.
def home_page(request):
    return render(request, "home.html")


def recipes_page(request):
    return render(request, "recipes.html")


def ingredients_page(request):
    ingredients_ = Ingredient.objects.all()
    return render(request, "ingredients.html", {"ingredients": ingredients_})
