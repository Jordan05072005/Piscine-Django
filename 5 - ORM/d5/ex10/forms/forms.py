from django import forms


class FormMovie(forms.Form):
    date_min = forms.DateField(label="Movies minimum release date", required=True)
    date_max = forms.DateField(label="Movies maximum release date", required=True)
    diameter = forms.IntegerField(label="Planet diameter greater than", required=True)
    gender = forms.ChoiceField(label="Gender", required=True)

    def __init__(self, gender_choice, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = gender_choice
