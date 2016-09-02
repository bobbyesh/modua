from django.forms import forms

class URLForm(forms.Form):
    url = forms.URLField(label='The page url', required=True)