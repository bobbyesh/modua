from django.test import TestCase, Client, RequestFactory
from django.http import JsonResponse
from .non_delimited_text import NonDelimitedText
import mock

class TestNonDelimitedText(TestCase):
    '''Test case for the NonDelimitedText class.'''

    test_string = "天下無雙"
    test_locale = "zh_HANT"
    test_list = ["天","天下","天下無","天下無雙"]

    def test_sub_units(self):
        '''Passes if a list built from the NonDelimitedText's sub_unit property is
        equal to the list it should be equal too, the test_list
        '''
        text = NonDelimitedText(self.test_string, self.test_locale)
        self.assertEqual(list(text.sub_units), self.test_list)

    def test_string_method(self):
        '''Passes if NonDelimitedText's __str__ representation is correct'''
        text = NonDelimitedText(self.test_string, self.test_locale)
        string = text.__str__()
        self.assertEqual(self.test_string, string)

    def test_eq_true(self):
        '''Passes if the __eq__ method of NonDelimitedText returns true when two objects of this type are equal'''
        text1 = NonDelimitedText(self.test_string, self.test_locale)
        text2 = NonDelimitedText(self.test_string, self.test_locale)
        self.assertTrue(text1 == text2)

    def test_eq_false(self):
        '''Passes if the __eq__ method of NonDelimitedText returns false when two objects of this type are not equal'''
        text1 = NonDelimitedText(self.test_string, self.test_locale)
        text2 = NonDelimitedText("Some other string", self.test_locale)
        self.assertFalse(text1 == text2)
