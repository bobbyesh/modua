from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import User, UserWord, PublicDefinition
from django.core.urlresolvers import reverse


DEBUG = True


class OwnerPermissionsTestCase(APITestCase):

    def setUp(self):
        john = User.objects.create_user(username='john', password='password')
        word = UserWord.objects.create(owner=john, word='foo', ease='easy')
        definition = PublicDefinition.objects.create(word=word, definition='bar')
        sally = User.objects.create_user(username='sally', password='password')

        word = UserWord.objects.create(word='public', ease='easy')
        definition = PublicDefinition.objects.create(word=word, definition='should be okay')


    def test_not_owner_cannot_read(self):
        '''John creates a word and then Sally tries to read it even though she shouldn't
        be able to.  Luckily she can't.'''
        client = APIClient()
        client.login(username='sally', password='password')
        url = reverse('word-detail', kwargs={'word': 'foo'})
        response = client.get(url, {'word': 'foo', 'username': 'john'})

        if DEBUG:
            self.debug_print(response, url)

        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)

    def test_owner_can_read(self):
        '''John creates a word and then accesses it successfully'''
        client = APIClient()
        client.login(username='john', password='password')
        url = reverse('word-detail', kwargs={'word': 'foo'})
        response = client.get(url, {'word': 'foo', 'username': 'john'})

        if DEBUG:
            self.debug_print(response, url)

        self.assertTrue(response.status_code == status.HTTP_200_OK)

    def test_non_owner_can_read_public_words(self):
        client = APIClient()
        url = reverse('word-detail', kwargs={'word': 'public'})
        response = client.get(url, {'word': 'public'})

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
