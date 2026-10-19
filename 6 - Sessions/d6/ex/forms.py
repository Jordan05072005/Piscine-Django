from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("username")
        password = cleaned.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return cleaned
        raise ValidationError("Username or Password is invalid")



class SignupForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
    password_verify = forms.CharField(label="Confirm Password", required=True, widget=forms.PasswordInput)


    def clean_username(self):
        username = self.cleaned_data['username']
        try :
            user = User.objects.get(username=username)
            if user:
                raise ValidationError("Username already exists")
        except User.DoesNotExist:
            return username

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        pwd2 = cleaned.get("password_verify")
        if pwd and pwd2 and pwd != pwd2:
            raise ValidationError("Les deux mots de passe ne correspondent pas.")
        return cleaned