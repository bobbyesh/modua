from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Definition, User, Language


class DefinitionTestCase(TestCase):

    def test_definition_users(self):
        '''Test that the Definition model's `users` ManyToMany field is operating correctly.'''
        john = User.objects.create_user(username='john', email='john@site.com', password='password')
        sally = User.objects.create_user(username='sally', email='sally@site.com', password='password')
        english = Language.objects.create(language='en')
        spanish = Language.objects.create(language='es')
        pairs = [('hey','hola'), ('lets go', 'vaminos'), ('school', 'escuela')]
        for word, translation in pairs:
            Definition.objects.create(
                language=english,
                target=spanish,
                word=word,
                translation=translation
            )


        instance = Definition.objects.filter(language=english, target=spanish, word='hey')[0]
        same, created = Definition.objects.get_or_create(
            language=instance.language,
            target=instance.target,
            word=instance.word,
            ease='hard'
        )
        same.users.add(john)

        same, created = Definition.objects.get_or_create(
            language=instance.language,
            target=instance.target,
            word=instance.word,
            ease='hard'
        )

        same.users.add(sally)


        different_ease1, created = Definition.objects.get_or_create(
            language=english,
            target=spanish,
            word='go',
            translation='va',
            ease='hard'
        )
        different_ease1.users.add(john)

        different_ease2, created = Definition.objects.get_or_create(
            language=english,
            target=spanish,
            word='go',
            translation='va',
            ease='easy'
        )
        different_ease2.users.add(sally)

        self.assertTrue(len(same.users.all()) == 2)
        self.assertTrue(len(different_ease1.users.all()) == 1)




class TestUserActivity(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', email='john@site.com', password='password')
        english = Language.objects.create(language='en')
        spanish = Language.objects.create(language='es')
        self.definition = Definition.objects.create(
            language=english,
            target=spanish,
            word='hey',
            translation='hola',
            contributor=self.user
        )
        self.definition = Definition.objects.create(
            language=english,
            target=spanish,
            word='how',
            translation='como',
            contributor=self.user
        )

    def test_user_create(self):
        result = Definition.objects.filter(contributor=self.user)
        self.assertTrue(len(result) == 2)


class TestOneLanguage(TestCase):

    def test_two_creates(self):
        english = Language.objects.create(language='en')
        Definition.objects.create(language=english, target=english, word='foo', translation='bar')
        Definition.objects.create(language=english, target=english, word='smoke', translation='screen')
        result = Definition.objects.all()
        self.assertTrue(len(result) == 2)

    def test_one_create(self):
        english = Language.objects.create(language='en')
        Definition.objects.create(language=english, target=english, word='foo', translation='bar')
        result = Definition.objects.all()
        self.assertFalse(len(result) == 2)

    def test__one_create(self):
        english = Language.objects.create(language='en')
        result = Language.objects.filter(language='en')
        self.assertTrue(len(result) == 1)

    def test_two_word_creates(self):
        english = Language.objects.create(language='en')
        Definition.objects.create(language=english, target=english, word='foo', translation='bar')
        Definition.objects.create(language=english, target=english, word='smoke', translation='screen')
        result = Definition.objects.filter(language=english)
        self.assertTrue(len(result) == 2)


class TestTwoLanguages(TestCase):

    def test_languages(self):
        english = Language.objects.create(language='en')
        spanish = Language.objects.create(language='es')
        Definition.objects.create(language=english, target=spanish, word='english_word1', translation='spanish_def1')
        Definition.objects.create(language=english, target=spanish, word='english_word2', translation='spanish_def2')

        Definition.objects.create(language=spanish, target=english, word='spanish_word1', translation='english_definition1')
        Definition.objects.create(language=spanish, target=english, word='spanish_word2', translation='english_definition2')
        english_result = Definition.objects.filter(language=english)
        spanish_result = Definition.objects.filter(language=spanish)
        self.assertTrue(len(english_result) == 2)
        self.assertTrue(len(spanish_result) == 2)
