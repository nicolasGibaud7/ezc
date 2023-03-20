# Generated by Django 3.2 on 2023-02-08 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list_generation', '0008_generatedshoppinglist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingListGeneration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(max_length=254)),
                ('shopping_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list_generation.shoppinglist')),
            ],
        ),
        migrations.DeleteModel(
            name='GeneratedShoppingList',
        ),
    ]