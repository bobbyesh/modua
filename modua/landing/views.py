import unicodedata
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from wordfencer.parser import ChineseParser

from .forms import SignupForm, AnnotationForm, SigninForm
from api.models import UserWordData, Definition


class IndexView(TemplateView):
    template_name = 'landing/index.html'


class ContactView(TemplateView):
    template_name = 'landing/contact.html'


class AboutView(TemplateView):
    template_name = 'landing/about.html'


class SigninView(FormView):
    model = User
    template_name = 'landing/login.html'
    form_class = SigninForm

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('webapp:home')
        else:
            return redirect('login')


class SignupView(CreateView):
    model = User
    template_name = 'landing/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('webapp:home')

    def form_valid(self, form):
        valid = super(SignupView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class SignupSuccessView(TemplateView):
    template_name = 'landing/success.html'


class LogoutView(TemplateView):
    template_name = 'landing/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DeleteAccountSuccessView(TemplateView):
    template_name = 'landing/delete_account_success.html'

    def get(self, request, *args, **kwargs):
        Definition.objects.filter(owner=request.user).delete()
        UserWordData.objects.filter(owner=request.user).delete()
        request.user.delete()
        return super().get(request, *args, **kwargs)
