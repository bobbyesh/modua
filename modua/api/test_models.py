from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Definition, User, Language, Article, Word


class DefinitionTestCase(TestCase):

    def test_definition_users(self):
        '''Test that the Definition model's `users` ManyToMany field is operating correctly.'''
        john = User.objects.create_user(username='john', email='john@site.com', password='password')
        sally = User.objects.create_user(username='sally', email='sally@site.com', password='password')

        word = Word.create(word='hey', language='en', definition_language='es', definition='hola', ease='hard')
        word.users.add(john)
        word.users.add(sally)

        self.assertTrue(len(word.users.all()) == 2)

    def test_different_ease_same_word(self):
        john = User.objects.create_user(username='john', email='john@site.com', password='password')
        sally = User.objects.create_user(username='sally', email='sally@site.com', password='password')

        hard = Word.create(word='hey', language='en', definition_language='es', definition='hola', ease='hard')
        easy = Word.create(word='hey', language='en', definition_language='es', definition='hola', ease='easy')

        hard.users.add(sally)
        easy.users.add(john)
        self.assertTrue(len(hard.users.all()) == 1)
        self.assertTrue(len(easy.users.all()) == 1)


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
