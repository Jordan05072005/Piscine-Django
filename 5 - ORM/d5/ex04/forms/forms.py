from django import forms


class RemoveMovie(forms.Form):
    title = forms.ChoiceField(choices=[])


    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].choices = choices