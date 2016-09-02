from django.views.generic.base import TemplateView
from core.utils import Token, get_api_response


class HomeView(TemplateView):

    template_name = 'webapp/home.html'


class ArticleView(TemplateView):

    template_name = 'webapp/sample.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        response = get_api_response('http://www.fox2008.cn/Article/2009/20090406000000_21827.html')

        content = response.text
        print(content)
        #title = self.get_title()
        #author = self.get_author()
        #tokens = self.get_tokens()
        return context