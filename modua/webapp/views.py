from django.views.generic import FormView
from django.views.generic.base import TemplateView
from core.utils import klassified
from core.services import fetch_article, tokenize_text


class URLImportView(FormView):
    

class HomeView(TemplateView):

    template_name = 'webapp/home.html'


class ArticleView(TemplateView):

    template_name = 'webapp/sample.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        text = fetch_article('http://www.fox2008.cn/Article/2009/20090406000000_21827.html', 'zh')
        context['tokens'] = klassified(tokenize_text(text))
        return context