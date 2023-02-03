"""ezcourses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from list_generation import views

urlpatterns = [
    url(r"^admin/", admin.site.urls, name="admin"),
    url(r"^$", views.home_page, name="home"),
    url("^recipes/$", views.recipes_page, name="recipes"),
    url("^ingredients/$", views.ingredients_page, name="ingredients"),
    url(
        "^ingredients/(\d+)/$",
        views.ingredient_details_page,
        name="ingredient_details",
    ),
    url("^recipes/(\d+)/$", views.recipe_details_page, name="recipe_details"),
    url("^add_recipe/(\d+)/$", views.add_recipe_page, name="add_recipe"),
]
