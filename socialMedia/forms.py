# blog/forms.py

from django import forms

class CanvasForm(forms.Form):
    body = forms.CharField()