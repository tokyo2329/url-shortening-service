from django import forms
from .models import Url


class UrlCreateForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ["original_url"]


class UrlEditForm(forms.ModelForm):
    class Meta:
        model = Url
        fields = ["expires_after", "expires_after_x_clicks"]
