from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import PublicDefinition, User, Article, Word


class ArticleTestCase(TestCase):
    def test_slugify(self):
        a = Article.objects.create(title='some title', text='some text')
        self.assertTrue(a.slug == 'some-title')


class PublicDefinitionPublicWordTestCase(TestCase):
    def test_create(self):
        word = Word.objects.create(word='hey')
        PublicDefinition.objects.create(word=word, definition='bar')
        result = PublicDefinition.objects.all()
        self.assertTrue(len(result) == 1)
