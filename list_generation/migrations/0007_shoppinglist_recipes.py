# Generated by Django 3.2 on 2023-02-03 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_generation', '0006_shoppinglist'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='recipes',
            field=models.ManyToManyField(to='list_generation.Recipe'),
        ),
    ]
