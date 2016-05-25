from django.test import TestCase, Client, RequestFactory
from rest_framework.response import Response


class TestRequests(TestCase):

    search_string = "天下無雙"
    search_locale = "zh_HANT"
    valid_search_url = "/api/0.1/search/"
    test_list = ["天", "天下", "天下無", "天下無雙"]
    test_definition = "There are no two things in the world that are the same"

    def setUp(self):
        '''Setup test case with a Client and RequestFactory to test views'''
        self.client = Client()
        self.factory = RequestFactory()

    def test_response_status_code_200(self):
        '''Passes if a generic GET request to 'oursite.com/search/foo' returns a
        response with status code 200.
        '''
        response = self.client.get(self.valid_search_url + self.search_string)
        self.assertEqual(response.status_code, 200, "GET" +
                         self.valid_search_url +
                         self.search_string +
                         " returns status code 200)")

    def test_response_is_type_RESPONSE(self):
        '''Passes if response is Django REST Framework Response object'''
        response = self.client.get(self.valid_search_url + self.search_string)
        self.assertIsInstance(response, Response,
                              "GET" + self.valid_search_url +
                              self.search_string +
                              " returns not a Response object")
