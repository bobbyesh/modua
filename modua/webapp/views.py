from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from api.models import Article, Language


from core.utils import klassified
from core.services import fetch_article, tokenize_text

from .forms import URLForm


@method_decorator(login_required, name='dispatch')
class HomeView(FormView, LoginRequiredMixin):

    template_name = 'webapp/home.html'
    login_url = 'landing/signin'
    form_class = URLForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        articles = self.request.user.api_article_owner.all()
        context['articles'] = articles
        context['user'] = self.request.user
        return context


    def form_valid(self, form):
        url = form.cleaned_data['url']
        user = self.request.user
        language = Language.objects.get(language='zh')
        article = Article.objects.filter(url=url)
        if article:
            text = article[0].text
        else:
            title, text = fetch_article(url, language='zh')

        Article.objects.get_or_create(text=text, url=url, language=language, owner=user)
        return super(HomeView, self).form_valid(form)




class ArticleView(TemplateView):

    template_name = 'webapp/sample.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        text = fetch_article('http://www.fox2008.cn/Article/2009/20090406000000_21827.html', 'zh')
        context['tokens'] = klassified(tokenize_text(text))
        return context
