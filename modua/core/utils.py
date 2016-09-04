# utils.py
'''A utility package for MODUA'''
import re
import configparser
import os
import requests
import unicodedata


class Token(object):
    '''Defines a class for use in templates.

    Effectively gives the `str` class a `klass` property.

    '''

    def __init__(self, string, klass):
        self.string = string
        self.klass = klass

    def __str__(self):
        return self.string

    def __eq__(self, string):
        self.string = string


def klassified(tokens):
    return [Token(elem, 'new') for elem in tokens]


def get_api_response(url):
    path = os.path.abspath(os.path.dirname(__file__)) + '/data/config.ini'
    config = configparser.ConfigParser()
    config.read(path)
    token = config['READABILITY']['token']
    base_url = 'https://readability.com/api/content/v1/parser'
    return requests.get(base_url, {'token': token, 'url': url})


def build_html(**kwargs):
    '''Builds an html element out of kwargs.

    The :arg:`tag` and :arg:`content` arguments are required.  :arg:`tag` defines what type of
    html tag, while :arg:`content` defines what is the actually content wrapped by the tag.
    Any other keyword-value pairs are taken as attributes of the tag.

    :Example:

        >>> build_html(tag='div', content='hello world!')
        '<div>hello world!</div>'
        
        >>> build_html(tag='div', content='hello world!', id='new', href='#')
        '<div id="new" href="#">'hello world!"</div>

    '''

    if 'tag' not in kwargs:
        raise Exception("Must contain kwarg `tag`.")
    if 'content' not in kwargs:
        raise Exception("Must contain kwarg `content`.")

    # You can't use python's keyword `class` as a kwarg, so use `cls` instead.
    # This code sets the 'class' kwarg to pass in for the html class attribute.
    if 'cls' in kwargs:
        kwargs['class'] = kwargs.pop('cls')

    tag = kwargs.pop('tag')
    content = kwargs.pop('content')

    attributes = ''
    for key, val in kwargs.items():
        attributes += ' {}="{}" '.format(key, val)

    open_tag = '<{tag} {attributes}>'.format(tag=tag, attributes=attributes)
    closing_tag = '</{tag}>'.format(tag=tag)

    return "{open_tag} {content} {closing_tag}".format(
        open_tag=open_tag,
        content=content,
        closing_tag=closing_tag
    )


def build_popup_html(word, definition):
    header = build_html(tag='h3',content=word)
    div = build_html(tag='div', content=definition)
    outer_span =  build_html(content=header + div, tag='div', name=word, cls='popup')
    return outer_span


def build_word_html(word):
    return build_html(content=word, tag='span', name=word, cls='word')


def segmentize(string):
    '''Yields a generator of string in segmented form.

    Example:
    If the object's string is 'ABCD', the generator will yield as follows:
        'ABCD' --> A AB ABC ABCD

    '''
    lexeme = ''
    for c in string:
        lexeme += c
        yield lexeme


def all_combinations(string):
    """Returns a set of yields all possible combinations of substrings."""
    s = set()
    for i in range(len(string)):
        for seg in segmentize(string[i:]):
            s.add(seg)
    return s


def is_delimited(tag):
    '''Returns True if the language tag identifies a space delimited
    language, otherwise returns False'''
    if type(tag) is not str:
        tag = str(tag)

    subtags = re.split('-', tag)
    if subtags[0] == 'en':
        return True
    if subtags[0] == 'zh':
        return False


def is_punctuation(char):
    if len(char) != 1:
        return False
    return unicodedata.category(char).startswith('P')

