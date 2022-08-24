from django import forms
from .models import Route


class RouteForm(forms.Form):
    start = forms.CharField(max_length=30)
    fin = forms.CharField(max_length=30)