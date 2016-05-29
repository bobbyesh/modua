from django.views.generic import ListView, DetailView, TemplateView, FormView


class HomeView(TemplateView):
    pass


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

