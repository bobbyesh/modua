#nondelimited_text.py

import django

class NonDelimitedText:
    '''A class for convenient processing of texts with no delimiter.

    A special property called sub_units allows easy iteration through the query
    choices defined by the MODUA algorithm for querying non-'spaced delimited'
    strings.


    '''

    def __init__(self, string, locale=None):
        '''Constructor that sets the string and locale (language) of the
        string
        '''
        self.string = string
        self.locale = locale

    @property
    def sub_units(self):
        '''Yields a generator of this object's string in segmented form.

        Example:
        If the object's string is 'ABCD', the generator will yield as follows:
            'ABCD' --> A AB ABC ABCD 

        '''
        lexeme = ''
        for c in self.string:
                lexeme += c
                yield lexeme

    def __str__(self):
        '''Returns the string only, not the locale'''
        return self.string

    def __eq__(self, compare):
        '''Returns true if the string and locale are equal to compare's string and 
        locale
        '''
        return (self.string == compare.string and 
                self.locale == compare.locale)
    

