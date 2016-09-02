from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import klassified
from core.services import fetch_article, tokenize_text


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView, LoginRequiredMixin):

    template_name = 'webapp/home.html'
    login_url = 'landing/signin'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        articles = self.request.user.api_article_owner.all()
        context['articles'] = articles
        import pdb;pdb.set_trace()
        return context

class ArticleView(TemplateView):

    template_name = 'webapp/sample.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        text = fetch_article('http://www.fox2008.cn/Article/2009/20090406000000_21827.html', 'zh')
        context['tokens'] = klassified(tokenize_text(text))
        return context
