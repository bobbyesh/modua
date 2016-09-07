from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import User, Language, Word, Definition
from django.core.urlresolvers import reverse


DEBUG = True


class OwnerPermissionsTestCase(APITestCase):

    def setUp(self):
        john = User.objects.create_user(username='john', password='password')
        language= Language.objects.create(language='en')
        word = Word.objects.create(owner=john, word='foo', language=language, ease='easy')
        definition = Definition.objects.create(word=word, language=language, definition='bar')
        sally = User.objects.create_user(username='sally', password='password')

        language= Language.objects.create(language='en')
        word = Word.objects.create(word='public', language=language, ease='easy')
        definition = Definition.objects.create(word=word, language=language, definition='should be okay')


    def test_not_owner_cannot_read(self):
        '''John creates a word and then Sally tries to read it even though she shouldn't
        be able to.  Luckily she can't.'''
        client = APIClient()
        client.login(username='sally', password='password')
        url = reverse('word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = client.get(url, {'language': 'en', 'word': 'foo', 'username': 'john'})

        if DEBUG:
            self.debug_print(response, url)

        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)

    def test_owner_can_read(self):
        '''John creates a word and then accesses it successfully'''
        client = APIClient()
        client.login(username='john', password='password')
        url = reverse('word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = client.get(url, {'language': 'en', 'word': 'foo', 'username': 'john'})

        if DEBUG:
            self.debug_print(response, url)

        self.assertTrue(response.status_code == status.HTTP_200_OK)

    def test_non_owner_can_read_public_words(self):
        client = APIClient()
        url = reverse('word-detail', kwargs={'language': 'en', 'word': 'public'})
        response = client.get(url, {'language': 'en', 'word': 'public'})

        if DEBUG:
            self.debug_print(response, url)

        self.assertTrue(response.status_code == status.HTTP_200_OK)


    def debug_print(self, response, url):
            print('\n==================================')
            print("non owner can read public")
            print(response)
            print(response.data)
            print('url == {}'.format(url))
            print('==================================\n\n')
