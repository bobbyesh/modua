import django
'''

    Request Structure:
    string: "word"
    langage: "langage"
    
    
    Example Structure:
    string: "天下無雙"
    locale: "zh_HANT"


    Actual string passed to view after urls.py:
    "?string=天下無雙&locale=zhHANT"

'''

class NonDelimitedText:

    def __init__(self, string, locale=None):
        self.string = string
        self.locale = locale

    @property
    def sub_units(self):
        ''' 'ABCD' --> A AB ABC ABCD '''
        lexeme = ''
        for c in self.string:
                lexeme += c
                yield lexeme

    def __str__(self):
        return self.string

    def __eq__(self, compare):
        return (self.string == compare.string and 
                self.locale == compare.locale)
    

