from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .forms import RegistrationForm, AnnotationForm

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


class AnnotationView(FormView):
    template_name = 'main_site/annotation.html'
    form_class = AnnotationForm
    success_url = '/home/annotate_complete/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            text = form.cleaned_data['text']
            request.session['text'] = text
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AnnotationCompleteView(TemplateView):
    template_name = 'main_site/annotate_complete.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['text'] = request.session['text']
        return self.render_to_response(context)


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

