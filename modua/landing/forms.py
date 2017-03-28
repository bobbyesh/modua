from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Field, Layout


class SigninForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # form_action associates a view name
        self.helper.form_action = 'signin'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))
        self.helper.layout = Layout(
            Div('username', css_class='top-margin'),
            Div('password', css_class='top-margin'),
        )


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = 'signup' # form_action associates a view name
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            'username',
            Div('email'),
            'password1',
            'password2',
        )


class AnnotationForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
