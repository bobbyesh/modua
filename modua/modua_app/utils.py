# utils.py
'''A utility package for MODUA'''
import re

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
