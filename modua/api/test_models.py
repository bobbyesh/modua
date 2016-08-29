from django.test import TestCase
from .models import Definition, User, Language


class TestUserActivity(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', email='john@site.com', password='password')
        english = Language.objects.create(language='en')
        spanish = Language.objects.create(language='es')
        self.definition = Definition.objects.create(
            source=english,
            target=spanish,
            word='hey',
            translation='hola',
            contributor=self.user
        )
        self.definition = Definition.objects.create(
            source=english,
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
        Definition.objects.create(source=english, target=english, word='foo', translation='bar')
        Definition.objects.create(source=english, target=english, word='smoke', translation='screen')
        result = Definition.objects.all()
        self.assertTrue(len(result) == 2)

    def test_one_create(self):
        english = Language.objects.create(language='en')
        Definition.objects.create(source=english, target=english, word='foo', translation='bar')
        result = Definition.objects.all()
        self.assertFalse(len(result) == 2)

    def test__one_create(self):
        english = Language.objects.create(language='en')
        result = Language.objects.filter(language='en')
        self.assertTrue(len(result) == 1)

    def test_two_word_creates(self):
        english = Language.objects.create(language='en')
        Definition.objects.create(source=english, target=english, word='foo', translation='bar')
        Definition.objects.create(source=english, target=english, word='smoke', translation='screen')
        result = Definition.objects.filter(source=english)
        self.assertTrue(len(result) == 2)


class TestTwoLanguages(TestCase):

    def test_languages(self):
        english = Language.objects.create(language='en')
        spanish = Language.objects.create(language='es')
        Definition.objects.create(source=english, target=spanish, word='english_word1', translation='spanish_def1')
        Definition.objects.create(source=english, target=spanish, word='english_word2', translation='spanish_def2')

        Definition.objects.create(source=spanish, target=english, word='spanish_word1', translation='english_definition1')
        Definition.objects.create(source=spanish, target=english, word='spanish_word2', translation='english_definition2')
        english_result = Definition.objects.filter(source=english)
        spanish_result = Definition.objects.filter(source=spanish)
        self.assertTrue(len(english_result) == 2)
        self.assertTrue(len(spanish_result) == 2)
