from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from .models import Definition, User, Language

class TestViews(APITestCase):


    def setUp(self):
        eng = Language.objects.create(language='en')
        zh = Language.objects.create(language='zh')

        Definition.objects.create(word="hello",
                                  translation="A greeting",
                                  language=eng,
                                  target=eng)

        Definition.objects.create(
            word="我",
            translation="I",
            language=zh,
            target=eng,
        )

        Definition.objects.create(
            word="爱",
            translation="love",
            language=zh,
            target=eng,
        )

        Definition.objects.create(
            word="中国",
            translation="China",
            language=zh,
            target=eng,
        )

        User.objects.create_user('john', 'john@gmail.com', 'password')


    def test_search_status_code_200(self):
        '''
        Passes if a valid search returns a status code of 200.
        '''
        response = self.client.get("/api/0.1/languages/en/hello/")
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        '''
        Passes if the json returned from a valid request is the correct json.
        '''
        response = self.client.get("/api/0.1/languages/en/hello/")
        self.assertContains(response, 'hello')

    def test_bad_term_search(self):
        '''
        Passes if a request for a word not in the dictionary returns a status code 404.
        '''
        response = self.client.get("/api/0.1/languages/en/term_not_in_DB/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_url(self):
        '''
        Passes if an invalid url returns a 404 response.
        '''
        response = self.client.get("/api/badurl/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_nondelimited_search(self):
        '''
        Passes if a request for a nondelimited word that isn't in the database returns a 404 response.
        '''
        response = self.client.get("/api/0.1/languages/zh/term_not_in_DB/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestLanguageAPI(APITestCase):


    def test_language_list_one_language(self):
        '''
        Passes if /languages/ returns the correct json.
        '''
        Language.objects.create(language='en')
        response = self.client.get("/api/0.1/languages/", format='json')
        json = response.json()
        results = json['results']
        expected = {'language': 'en'}
        for d in results:
            self.assertTrue(d['language'] == expected['language'])


    def test_language_list_two_languages(self):
        '''
        Passes if /languages/ returns the correct json.
        '''
        Language.objects.create(language='en')
        Language.objects.create(language='zh')
        response = self.client.get("/api/0.1/languages/", format='json')
        json = response.json()
        results = json['results']
        results = sorted(results, key=lambda x: x['language'])
        expected = [{'language': 'en'}, {'language': 'zh'}]
        expected = sorted(expected, key=lambda x: x['language'])
        for x,y in zip(results, expected):
            self.assertTrue(x['language'] == y['language'])
