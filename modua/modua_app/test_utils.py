from django.test import SimpleTestCase
from .utils import segmentize, is_delimited


class TestUtils(SimpleTestCase):
    '''This test case tests MODUA's utils package.'''

    test_string = "天下無雙"
    test_locale = "zh_HANT"
    test_list = ["天", "天下", "天下無", "天下無雙"]

    def test_build_generator(self):
        '''Test that the generator from search_segments yields a generator
        that produces the correct order
        '''
        segments = segmentize(self.test_string)
        self.assertEqual(list(segments), self.test_list)

    def test_is_delimited(self):
        '''Test that the is_delimited function works'''
        self.assertTrue(is_delimited('en-US'))
        self.assertFalse(is_delimited('zh-Hanz'))
