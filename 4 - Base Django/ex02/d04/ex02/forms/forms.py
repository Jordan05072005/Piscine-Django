from django import forms


class BasicForm(forms.Form):
    text = forms.CharField(label="Text", max_length=100)