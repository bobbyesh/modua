import json
from rest_framework.test import APITestCase, APIRequestFactory

from .models import Definition, User, Language
from .views import LanguageListView, DefinitionListView


class TestLanguageListView(APITestCase):


    def setUp(self):
        Language.objects.create(language='en')
        Language.objects.create(language='zh')

    def test_list_results(self):
        view = LanguageListView.as_view()
        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/')
        response = view(request)
        self.assertContains(response, 'en')
        self.assertContains(response, 'zh')


class TestDefinitionListView(APITestCase):


    def setUp(self):
        language = Language.objects.create(language='en')
        Definition.objects.create(
            source=language,
            target=language,
            word='cool',
            translation='not hot',
        )

        Definition.objects.create(
            source=language,
            target=language,
            word='building',
            translation='a thing in cities',
        )

        chinese = Language.objects.create(language='zh')

        Definition.objects.create(
            source=chinese,
            target=chinese,
            word='chineseword',
            translation='some translation',
        )
        view = DefinitionListView.as_view()
        factory = APIRequestFactory()
        request = factory.get('/api/0.1/languages/en/cool/')
        self.response = view(request, language='en', word='cool')

    def test_does_contain_word(self):
        self.assertContains(self.response, 'cool')

    def test_does_not_contain_different_word_same_language(self):
        self.assertNotContains(self.response, 'building')

    def test_does_not_contain_different_language(self):
        self.assertNotContains(self.response, 'chineseword')
