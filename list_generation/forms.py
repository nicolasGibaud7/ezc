from django import forms

from list_generation.models import ShoppingListGeneration


class ShoppingListGenerationForm(forms.ModelForm):
    class Meta:
        model = ShoppingListGeneration
        fields = (
            "format_choice",
            "sending_method",
            "mail",
        )
        widgets = {
            "mail": forms.EmailInput(
                attrs={
                    "id": "id_email",
                    "placeholder": "Email address",
                    "class": "form-control input-lg mt-2",
                }
            ),
            "format_choice": forms.Select(
                attrs={"class": "form-select form-select-lg mt-2"}
            ),
            "sending_method": forms.Select(
                attrs={"class": "form-select form-select-lg mt-2"}
            ),
        }
        error_messages = {
            "mail": {
                "required": "Please enter your email address",
                "invalid": "Please enter a valid email address",
            },
            "format_choice": {"required": "Please select a format"},
            "sending_method": {"required": "Please select a sending method"},
        }
