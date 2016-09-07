from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Definition, User, Language, Article, Word


class ArticleTestCase(TestCase):

    def test_slugify(self):
        l = Language.objects.create(language='en')
        a = Article.objects.create(title='some title', text='some text', language=l)
        self.assertTrue(a.slug == 'some-title')


class DefinitionWordLanguageTestCase(TestCase):

    def test_create(self):
        english = Language.objects.create(language='en')
        word = Word.objects.create(word='hey', language=english)
        Definition.objects.create(language=english, word=word, definition='bar')
        result = Definition.objects.all()
        self.assertTrue(len(result) == 1)
