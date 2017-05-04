# utils.py
'''A utility package for MODUA'''
import configparser
import os
import requests
import unicodedata
import calendar
from datetime import datetime, timedelta
from django.db.utils import IntegrityError
from core.exceptions import Raise403
from wordfencer.parser import ChineseParser
from api import models


def get_object_or_403(model, message='HTTP 403: Forbidden', **kwargs):
    try:
        obj = model.objects.create(**kwargs)
    except IntegrityError:
        raise Raise403(detail=message)

    return obj


class Token(object):
    '''Defines a class for use in templates.

    Effectively gives the `str` class a `klass` property.

    '''

    def __init__(self, string, position):
        self.string = string
        self.position = position

    def __str__(self):
        return self.string

    def __eq__(self, string):
        self.string = string


def segmentize(string):
    """Yields a generator of string in segmented form.

    Example:
    If the object's string is 'ABCD', the generator will yield as follows:
        'ABCD' --> A AB ABC ABCD

    """
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


def is_punctuation(char):
    """We use unicode data here because it also includes CJK punctuation."""
    if len(char) != 1:
        return False
    return unicodedata.category(char).startswith('P')


def tokenize_text(text):
    p = ChineseParser()
    tokens = []
    for string in text.split():
        tokens += p.parse(string)

    return tokens


def is_valid_word(word):
    type_ = type(word)
    if type_ is models.UserWordData or type_ is models.Word:
        word = word.word
    return not is_punctuation(word) and word.strip()


def get_month_range():
    now = datetime.now()
    first_day, last_day = calendar.monthrange(now.year, now.month)
    return datetime(now.year, now.month, 1), datetime(now.year, now.month, last_day)


def get_week_range():
    now = datetime.now()
    weekday = calendar.weekday(now.year, now.month, now.day)
    days_from_monday = timedelta(days=weekday)
    days_until_sunday = timedelta(days=7-weekday)
    first = now - days_from_monday
    last = now + days_until_sunday
    return first, last


def get_day_range():
    now = datetime.now()
    return (
            datetime(now.year, now.month, now.day),
            datetime(now.year, now.month, now.day + 1) - timedelta(seconds=1) # Just before midnight
           )

