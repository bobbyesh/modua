from collections import Counter
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from api.models import Article, PublicWord, PublicDefinition, UserWord, UserDefinition
from core.services import fetch_article
from webapp.forms import ArticleForm


@method_decorator(login_required, name='dispatch')
class HomeView(FormView, LoginRequiredMixin):
    template_name = 'webapp/home.html'
    login_url = 'landing/login'
    form_class = ArticleForm
    success_url = reverse_lazy('webapp:home')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        articles = self.request.user.api_article_owner.all()
        context['articles'] = articles
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        user = self.request.user
        url = form.cleaned_data['url']
        title = form.cleaned_data['title']
        body = form.cleaned_data['body']
        # If this article is new, add the words to this user's db
        # We do this now so we don't have to do when loading the article for them
        # to read later.
        article, created = Article.objects.get_or_create(title=title, body=body, url=url, owner=user)
        if created:
            for token in article.as_tokens():
                word, created = UserWord.objects.get_or_create(word=token, owner=user)
                if created:
                    definitions = []
                    try:
                        public_word = PublicWord.objects.get(word=token)
                        pinyin = public_word.pinyin
                        word.pinyin = pinyin
                        word.ease = 0
                        word.save()
                        word.articles.add(article)
                        for public_definition in PublicDefinition.objects.filter(word=public_word):
                            UserDefinition.objects.get_or_create(word=word, owner=user, definition=public_definition)
                    except PublicWord.DoesNotExist:
                        pass

        return super(HomeView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleView(TemplateView):
    template_name = 'webapp/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        article = Article.objects.get(slug=self.kwargs['slug'], owner=self.request.user)
        userwords = article.userword_set.all()
        words = []
        for word in article.as_tokens():
            try:
                userword = userwords.get(word=word)
            except ObjectDoesNotExist:
                userword = word

            words.append(userword)

        context['entries'] = words
        # The e.ease int is turned into a string because Django templates don't like
        # integers as dictionary keys
        context['counts'] = Counter(str(e.ease) for e in context['entries'] if hasattr(e, 'ease'))
        return context


@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
    template_name = 'webapp/account.html'
