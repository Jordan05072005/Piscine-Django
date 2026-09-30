from django import forms


class RemoveMovie(forms.Form):
    title = forms.ChoiceField(choices=[])


    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].choices = choices


class UpdateMovie(RemoveMovie):
    opening_crawl = forms.CharField(widget=forms.Textarea)