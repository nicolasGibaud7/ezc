from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home_page(request):
    return render(request, "home.html")


def recipes_page(request):
    return render(request, "recipes.html")


def ingredients_page(request):
    return render(request, "ingredients.html")
