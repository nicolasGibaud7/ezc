# Generated by Django 3.2 on 2023-02-03 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_generation', '0005_recipe_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
