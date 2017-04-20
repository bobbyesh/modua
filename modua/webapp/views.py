from collections import defaultdict
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q, Max
from django.core.exceptions import ObjectDoesNotExist

from api.models import Article, UserWordData, Definition, UserWordTimeStamp
from webapp.forms import ArticleForm
from core.services import YouDaoAPI
from core.utils import is_valid_word, get_month_range, get_week_range, get_day_range


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
        Article.objects.create(title=title, body=body, url=url, owner=user)
        return super(HomeView, self).form_valid(form)


@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ArticleView(TemplateView):
    template_name = 'webapp/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        article = Article.objects.get(slug=self.kwargs['slug'], owner=self.request.user)
        article_words = []
        dictionary_entries = []
        for word in article.words:
            if is_valid_word(word):
                datum, _ = UserWordData.objects.get_or_create(word=word, owner=self.request.user)
                definitions = self.get_definitions(word)
                definitions.pinyin_list = [p['pinyin'] for p in definitions.values('pinyin').distinct()]
                definitions.word = word
                dictionary_entries.append(definitions)
            else:
                datum = word

            article_words.append(datum)

        context['dictionary_entries'] = dictionary_entries
        context['article_words'] = article_words
        return context

    def get_definitions(self, word):
        definitions = Definition.objects.filter(word=word)
        # TODO: Make a more sophisticated decision process for API calls
        # We go to the YouDao api if we can't find any definitions for this word
        if not definitions:
            api_data = YouDaoAPI.get_word(word)
            for definition in api_data['definitions']:
                pinyin = api_data['pinyin']
                Definition.objects.create(word=word, definition=definition, pinyin=pinyin, owner=None)

        return Definition.objects.filter(word=word) \
                                 .filter(Q(owner=self.request.user) | Q(owner=None))


@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
    template_name = 'webapp/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['email'] = self.request.user.email
        return context


@method_decorator(login_required, name='dispatch')
class ChangeUsernameView(FormView):
    template_name = 'webapp/change_username.html'
    form_class = UserChangeForm


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(FormView):
    template_name = 'webapp/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('webapp:account')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class DeleteAccountView(TemplateView):
    template_name = 'webapp/delete_account.html'


@method_decorator(login_required, name='dispatch')
class DeleteAccountRedirectView(RedirectView):
    url = reverse_lazy('delete_account_success')


@method_decorator(login_required, name='dispatch')
class UserStatsView(TemplateView):
    template_name = 'webapp/user_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = UserWordData.objects.filter(owner=self.request.user)
        new = queryset.filter(ease=0)
        hard = queryset.filter(ease=1)
        easy = queryset.filter(ease=2)
        known = queryset.filter(ease=3)

        context['word_counts'] = dict()
        context['word_counts']['new'] = len(new)
        context['word_counts']['hard'] = len(hard)
        context['word_counts']['easy'] = len(easy)
        context['word_counts']['known'] = len(known)

        queryset = UserWordTimeStamp.objects.filter(owner=self.request.user)
        context['learned_this_month'] = self.get_final_known_count(queryset.filter(timestamp__range=get_month_range()))
        context['learned_this_week'] = self.get_final_known_count(queryset.filter(timestamp__range=get_week_range()))
        context['learned_today'] = self.get_final_known_count(queryset.filter(timestamp__range=get_day_range()))
        return context

    def get_final_known_count(self, queryset):
        words = queryset.values('word').distinct()
        count = 0
        for word in words:
            word = word['word']
            most_recent_time = queryset.filter(word=word) \
                                       .aggregate(Max('timestamp'))
            most_recent_time = most_recent_time['timestamp__max']
            try:
                most_recent_instance = queryset.get(timestamp=most_recent_time, word=word)
                if most_recent_instance.ease == 3:
                    count += 1
            except ObjectDoesNotExist:
                pass

        return count