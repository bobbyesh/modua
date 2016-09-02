from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import klassified
from core.services import fetch_article, tokenize_text


class HomeView(TemplateView):

    template_name = 'webapp/home.html'


class ArticleView(TemplateView):

    template_name = 'webapp/sample.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        text = fetch_article('http://www.fox2008.cn/Article/2009/20090406000000_21827.html', 'zh')
        context['tokens'] = klassified(tokenize_text(text))
        return context


class CollectionView(TemplateView, LoginRequiredMixin):

    template_name = 'webapp/collection.html'
    login_url = 'landing/signin'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super(CollectionView, self).get_context_data(**kwargs)
        articles = self.request.user.api_owner_article.all()
        context['articles'] = articles
        import pdb;pdb.set_trace()
        return context
