from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email']

class AnnotationForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
