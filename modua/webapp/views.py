from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.o

class HomeView(TemplateView):

    template_name = 'webapp/home.html'

class ArticleView(TemplateView):

    template_name = 'webapp/article.html'
