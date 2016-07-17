from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from .forms import RegistrationForm

import pdb

class HomeView(TemplateView):
    template_name = 'main_site/home.html'

class RegistrationView(FormView):
    template_name = 'main_site/register.html'
    form_class = RegistrationForm
    success_url = '/home/success/'

    def form_valid(self, form):
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create(username=username,
                                email=email,
                                password=password)
        return super(RegistrationView, self).form_valid(form)

class RegistrationSuccessView(TemplateView):
    template_name = 'main_site/success.html'

class LoginView(TemplateView):
    pass


class UserPageView(TemplateView):
    pass


class WordListView(ListView):
    pass


class WordDetailView(DetailView):
    pass

class AddDefinitionView(FormView):
    pass

