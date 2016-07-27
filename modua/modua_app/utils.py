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
