from django import forms


class ShoppingListGenerationForm(forms.Form):
    mail = forms.EmailField()
    format_choice = forms.ChoiceField(choices=[("txt", "txt"), ("pdf", "pdf")])
    sending_method = forms.ChoiceField(
        choices=[("email", "email"), ("download", "download")]
    )
