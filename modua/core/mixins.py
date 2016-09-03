# mixins.py

from api.models import Article
from core.services import fetch_article


class ArticleViewMixin(object):

    def save_or_create_article(self, language, url, user):
        article = Article.objects.filter(url=url)
        if not article:
            text = fetch_article(url, language)
            Article.objects.create(text=text, url=url, language=self.language, owner=user)
