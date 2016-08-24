from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Field, Layout

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # form_action associates a view name
        self.helper.form_action = 'signup'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div('username', css_class='top-margin'),
            Div('email', css_class='top-margin'),
            Div('password', css_class='top-margin'),
        )


class AnnotationForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
