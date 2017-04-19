# api.py
"""Defines a YouDaoAPI class for accessing the public youdao.com api.

Instantiating With API Key
==========================

>>> youdao = YouDaoAPI()


Making Queries
==============

The `get` method returns a dictionary with the
word, its definitions, and the pinyin.
After instantiating with one of the above methods:

    >>> query = youdao.get('你好')
    >>> query
    {'word': '你好', 'pinyin': 'nǐ hǎo', 'def': ['hello；hi']}
    
"""


from urllib.parse import quote
import requests
from django.conf import settings


class YouDaoAPI(object):
    '''
    ..TODO:  Detect when the translation doesn't actually exist.
    
    '''

    error_messages = {
        0: 'Normal',
        20: 'The request string was too long',
        30: 'Unable to efficiently translate',
        40: 'Unsupported language type',
        50: 'Invalid key',
        60: 'No dictionary results',
    }

    key = settings.YOUDAO_KEY
    key_from = settings.YOUDAO_KEYFROM

    @staticmethod
    def get_word(word):
        if type(word) is not str:
            try:
                word = str(word)
            except ValueError:
                raise ValueError('word arg in YouDaoAPI.get_word must be str or have __str__ defined')
        json = YouDaoAPI.get_json(word)
        if 'basic' not in json:
            raise Exception('This request did not return basic definitions.  '
                            'Perhaps it was not a single word?')

        try:
            definitions = json['basic']['explains']
            pinyin = json['basic']['phonetic'] if 'phonetic' in json['basic'] else 'no pinyin'
        except KeyError:
            pass

        return {
            'definitions': definitions,
            'pinyin': pinyin,
            'word': word
        }

    @staticmethod
    def get_json(word):
        url = YouDaoAPI.url(word)
        response = requests.get(url)
        return response.json()

    @staticmethod
    def get_jsonp(word):
        url = YouDaoAPI.url(word, doctype='jsonp')
        response= requests.get(url)
        return response.json()

    @staticmethod
    def url(word, doctype='json'):
        return ('http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s'
                '&type=data&doctype=%s&version=1.1&q=') % (YouDaoAPI.key_from, YouDaoAPI.key, doctype) + quote(word)

    @staticmethod
    def handle_error(json):
        code = json['error_code']
        if code != 0:
            raise Exception(YouDaoAPI.error_messages[code])