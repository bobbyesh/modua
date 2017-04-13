from crispy_forms.layout import Submit
from django import forms
from crispy_forms.helper import FormHelper
from api.models import Article

class URLForm(forms.Form):
    url = forms.URLField(label='Type the page url here', required=True)

    def __init__(self, *args, **kwargs):
        super(URLForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Import'))


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'url']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Import'))
