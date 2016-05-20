from django.test import TestCase, Client, RequestFactory
from django.db import models
from django.http import JsonResponse
import mock


class TestRequests(TestCase):

    test_string = "天下無雙"
    test_locale = "zh_HANT"
    test_list = ["天","天下","天下無","天下無雙"]
    test_definition = "There are no two things in the world that are the same"

    def setUp(self):
        '''Setup this test case with a Client and RequestFactory to test views'''
        self.client = Client()
        self.factory = RequestFactory()

    def test_request_successful(self):
        '''Passes if a generic GET request to 'oursite.com/lookup/' returns a
        response with status code 200.
        '''
        response = self.client.get("/lookup/foo")
        self.assertEqual(response.status_code, 200, "/lookup/foo resturns status code 200)")

    def test_response_is_JsonResponse(self):
        response = self.client.get(self.build_valid_url())
        self.assertIsInstance(response, JsonResponse)

    def build_valid_url(self):
        '''Returns a string that is a valid GET request and url'''
        string_pair = "string=" + self.test_string
        locale_pair =  "locale=" + self.test_locale
        url = "/lookup/?" + string_pair + "&" + locale_pair
        return url

