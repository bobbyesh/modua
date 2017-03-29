from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import User, UserWord, UserDefinition, PublicWord, PublicDefinition
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token


DEBUG = True


class OwnerPermissionsTestCase(APITestCase):

    def setUp(self):
        john = User.objects.create_user(username='john', password='password')
        word = UserWord.objects.create(owner=john, word='foo', ease='easy')
        definition = UserDefinition.objects.create(word=word, definition='bar')
        word = PublicWord.objects.create(word='public')
        definition = PublicDefinition.objects.create(word=word, definition='should be okay')
        sally = User.objects.create_user(username='sally', password='password')

    def test_not_owner_cannot_read(self):
        '''John creates a word and then Sally tries to read it even though she shouldn't
        be able to.  Luckily she can't.'''
        client = APIClient()
        client.login(username='sally', password='password')
        kwargs = {'word': 'foo'}
        url = reverse('user-word-detail', kwargs=kwargs)
        response = client.get(url, kwargs)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_read(self):
        '''John creates a word and then accesses it successfully'''
        client = APIClient()
        token = Token.objects.get(user__username='john')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        client.login(username='john', password='password')
        kwargs = {'word': 'foo'}
        url = reverse('user-word-detail', kwargs=kwargs)
        response = client.get(url, kwargs)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_can_read_public_words(self):
        client = APIClient()
        kwargs = {'word': 'public'}
        url = reverse('public-word-detail', kwargs=kwargs)
        response = client.get(url, kwargs)
        self.assertTrue(response.status_code == status.HTTP_200_OK)
