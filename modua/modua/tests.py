from django.test import TestCase, Client, RequestFactory
from django.db import models
from modua_app.string_processor import QueryString

class TestDictionary(models.Model):
    word = models.CharField(max_length=15)
    definition = models.CharField(max_length=100)

class TestRequests(TestCase):
        
    test_string = "天下無雙"
    test_locale = "zh_HANT"

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_request_successful(self):
        response = self.client.get("/lookup/foo")
        self.assertEqual(response.status_code, 200, "/lookup/foo resturns status code 200)")

    def test_string_processor(self):
        request = self.get_basic_request()
        query_from_request = QueryString.from_request(request)
        query_from_manual = QueryString(self.test_string, self.test_locale)
        self.assertEqual(query_from_request, query_from_manual)
    
    def get_basic_request(self):
        string_pair = "string=" + self.test_string
        locale_pair =  "locale=" + self.test_locale
        url = "/lookup/?" + string_pair + "&" + locale_pair
        request = self.factory.get(url)
        return request;


    def test_query_string_iter(self):
        query = QueryString(self.test_string, self.test_locale)
        test_list = ["天下無雙","天下無","天下","天"]
        self.assertEqual(list(query), test_list)

