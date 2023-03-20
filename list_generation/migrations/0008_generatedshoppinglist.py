# Generated by Django 3.2 on 2023-02-08 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('list_generation', '0007_shoppinglist_recipes'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedShoppingList',
            fields=[
                ('shoppinglist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='list_generation.shoppinglist')),
            ],
            bases=('list_generation.shoppinglist',),
        ),
    ]