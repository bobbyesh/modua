from django.views.generic import View, ListView, DetailView, TemplateView, FormView
from django.contrib.auth.models import User
from django.http import HttpResponse


class HomeView(TemplateView):
    template_name = "main_site/home.html"

class RegistrationView(View):
    def get(self, request):
        return HttpResponse('registration page!')

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

