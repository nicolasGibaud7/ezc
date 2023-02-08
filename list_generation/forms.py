from django import forms

from list_generation.models import ShoppingListGeneration


class ShoppingListGenerationForm(forms.ModelForm):
    class Meta:
        model = ShoppingListGeneration
        fields = ("mail", "format_choice", "sending_method")
        widgets = {"mail": forms.EmailInput(attrs={"id": "id_email"})}
        error_messages = {
            "mail": {
                "required": "Please enter your email address",
                "invalid": "Please enter a valid email address",
            },
            "format_choice": {"required": "Please select a format"},
            "sending_method": {"required": "Please select a sending method"},
        }
