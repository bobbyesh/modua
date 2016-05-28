# utils.py
'''A utility package for MODUA'''

def search_segments(string):
    '''Yields a generator of string in segmented form.

    Example:
    If the object's string is 'ABCD', the generator will yield as follows:
        'ABCD' --> A AB ABC ABCD

    '''
    lexeme = ''
    for c in string:
        lexeme += c
        yield lexeme
