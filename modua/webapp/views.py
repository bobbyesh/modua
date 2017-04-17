from collections import Counter
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import ensure_csrf_cookie

from api.models import Article, PublicWord, PublicDefinition, UserWord, UserDefinition
from webapp.forms import ArticleForm
from core.services import YouDaoAPI
from core.utils import is_valid_word

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
                user_word, created = UserWord.objects.get_or_create(word=token, owner=user)
                user_word.articles.add(article)
                if created:
                    user_word.ease = 0
                    user_word.save()
                    public_words = PublicWord.objects.filter(word=user_word.word)
                    if public_words:
                        self.load_user_data_with_public_data(public_words, user_word)
                    else:
                        HomeView.load_public_data_with_api_data(token)
                        public_words = PublicWord.objects.filter(word=user_word.word)
                        self.load_user_data_with_public_data(public_words, user_word)

        return super(HomeView, self).form_valid(form)

    def load_user_data_with_public_data(self, public_words, user_word):
        """For all words in public_words, find their public definitions and save them as
        user definitions.  Associate the new definitions with the user_word and owner.
        
        """
        for public_word in public_words:
            for public_definition in PublicDefinition.objects.filter(word=public_word):
                UserDefinition.objects.get_or_create(
                    word=user_word,
                    owner=self.request.user,
                    definition=public_definition.definition,
                    pinyin=public_definition.pinyin
                )

    @staticmethod
    def load_public_data_with_api_data(word):
        if not is_valid_word(word):
            return
        else:
            api_response = YouDaoAPI.get_word(word)
            if 'definitions' in api_response:
                definitions = api_response['definitions']
                pinyin = api_response['pinyin']
                public_word, _ = PublicWord.objects.get_or_create(word=word)
                for definition in definitions:
                    PublicDefinition.objects.get_or_create(word=public_word, definition=definition, pinyin=pinyin)
                    print(definition)


@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ArticleView(TemplateView):
    template_name = 'webapp/article.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        article = Article.objects.get(slug=self.kwargs['slug'], owner=self.request.user)
        user_words = article.userword_set.all()
        words = []
        for word in article.as_tokens():
            try:
                user_word = user_words.get(word=word)
            except ObjectDoesNotExist:
                user_word = word

            words.append(user_word)

        entries = []
        for word in user_words:
            definitions = word.userdefinition_set.all()
            unique_pinyins = set(d.pinyin for d in definitions)
            pinyin_definitions = []
            for pinyin in unique_pinyins:
                tup = (pinyin, definitions.filter(pinyin=pinyin))
                pinyin_definitions.append(tup)

            entries.append({
                'entry': word,
                'pinyin_definitions': pinyin_definitions,
            })

        words = [{'word': word} if is_valid_word(word) else {'other': word} for word in words]
        context['article_words'] = words
        context['dictionary_entries'] = entries
        # The e.ease int is turned into a string because Django templates don't like
        # integers as dictionary keys
        context['counts'] = Counter(str(e['entry'].ease) for e in context['dictionary_entries'])
        return context


@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
    template_name = 'webapp/account.html'


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
        queryset = UserWord.objects.filter(owner=self.request.user)
        new = queryset.filter(ease=0)
        hard = queryset.filter(ease=1)
        easy = queryset.filter(ease=2)
        known = queryset.filter(ease=3)

        context['word_counts'] = dict()
        context['word_counts']['new'] = len(new)
        context['word_counts']['hard'] = len(hard)
        context['word_counts']['easy'] = len(easy)
        context['word_counts']['known'] = len(known)
        return context