from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import User, Language, Word, Definition
from django.core.urlresolvers import reverse

DEBUG = True


class OwnerPermissionsTestCase(APITestCase):
    pass

    def test_not_owner_cannot_read(self):
        '''John creates a word and then Sally tries to read it even though she shouldn't
        be able to.  Luckily she can't.'''
        john = User.objects.create(username='john', password='password')
        language= Language.objects.create(language='en')
        word = Word.objects.create(user=john, word='foo', language=language, ease='easy')
        definition = Definition.objects.create(word=word, language=language, definition='bar')
        sally = User.objects.create(username='sally', password='password')
        client = APIClient()
        client.login(username='sally', password='password')
        url = reverse('word-detail', kwargs={'language': 'en', 'word': 'foo'})
        response = client.get(url, {'username': 'john'})

        if DEBUG:
            print(response)
            print(response.data)
            print('url == {}'.format(url))

        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)
