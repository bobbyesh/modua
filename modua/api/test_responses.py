from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse
from .models import User, PublicWord, UserWord, UserDefinition, PublicDefinition



class UserDefinitionDetailTestCase(APITestCase):

    def setUp(self):
        username = 'john'
        password = 'password'
        john = User.objects.create_user(username=username, email='jdoe@gmail.com', password=password)
        word = UserWord.objects.create(word='foo', owner=john)
        definition = UserDefinition.objects.create(word=word, definition='bar', owner=john)

        token = Token.objects.get(user__username=username)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client.login(username=username, password=password)
        self.word = word
        self.client = client
        self.definition = definition

    def test_get_definition(self):
        kwargs= {'pk': self.definition.pk }
        url = reverse('user-definition-detail', kwargs=kwargs)
        response = self.client.get(url, kwargs)
        self.assertContains(response, 'bar')

    def test_delete_definition(self):
        kwargs= {'word': 'foo'}
        url = reverse('user-definition-list')
        kwargs= {'definition': 'bar', 'word': 'foo', 'username': 'john'}
        response = self.client.delete(url, kwargs)
        queryset = PublicDefinition.objects.all()
        self.assertQuerysetEqual(queryset, [])

    def test_can_not_delete_public(self):
        word = PublicWord.objects.create(word='notfoo')
        PublicDefinition.objects.create(
            word=word,
            definition='public',
        )

        kwargs= {'word': 'notfoo'}
        url = reverse('user-definition-list')
        response = self.client.delete(url, kwargs)

        result = PublicDefinition.objects.filter(
            word=word,
        )

        self.assertTrue(len(result) != 0)


class TestPublicRequests(APITestCase):

    def setUp(self):
        for chinese_word, english_word in [("我", "I"), ("爱", "love"), ("中国", "China")]:
            word = PublicWord.objects.create(word=chinese_word)
            definition = PublicDefinition.objects.create(definition=english_word, word=word)


    def test_search_status_code_200(self):
        '''
        Passes if a valid search returns a status code of 200.
        '''
        response = self.client.get("/api/0.1/word/我/")
        self.assertEqual(response.status_code, 200)

    def test_term_search(self):
        '''
        Passes if the json returned from a valid request is the correct json.
        '''
        response = self.client.get("/api/0.1/word/我/")
        self.assertContains(response, '我')

    def test_bad_term_search(self):
        '''
        Passes if a request for a word not in the dictionary returns a status code 404.
        '''
        response = self.client.get("/api/0.1/word/term_not_in_DB/", format='json')
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
        response = self.client.get("/api/0.1/word/term_not_in_DB/", format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
