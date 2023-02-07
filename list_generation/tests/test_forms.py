from django.test import TestCase

from list_generation.forms import ShoppingListGenerationForm


class ShoppingListGenerationFormTest(TestCase):
    def test_form_renders_mail_field_input(self):
        form = ShoppingListGenerationForm()
        self.assertIn('type="email"', form.as_p())

    def test_form_renders_format_choice_field_input(self):
        form = ShoppingListGenerationForm()
        self.assertIn('select name="format_choice"', form.as_p())

    def test_form_renders_sending_method_field_input(self):
        form = ShoppingListGenerationForm()
        self.assertIn('select name="sending_method"', form.as_p())
