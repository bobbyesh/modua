from django.test import TestCase, Client, RequestFactory
from rest_framework.response import Response


class TestRequests(TestCase):

    search_string = "天下無雙"
    search_locale = "zh_HANT"
    test_list = ["天","天下","天下無","天下無雙"]
    test_definition = "There are no two things in the world that are the same"

    def setUp(self):
        '''Setup this test case with a Client and RequestFactory to test views'''
        self.client = Client()
        self.factory = RequestFactory()

    def test_request_to_api_search(self):
        '''Passes if a generic GET request to 'oursite.com/search/foo' returns a
        response with status code 200.
        '''
        response = self.client.get("/api/search/" + self.search_string)
        self.assertEqual(response.status_code, 200, "api/search/" + self.search_string + " returns status code 200)")
