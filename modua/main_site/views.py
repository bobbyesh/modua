from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.contrib.auth.models import User


class HomeView(TemplateView):
    template_name = "main_site/home.html"




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

