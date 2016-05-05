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

class QueryString:

    def __init__(self, string, locale=None):
        self.string = string
        self.locale = locale

    @classmethod
    def from_request(cls, request):
        string = cls.string_from_request(cls, request)
        locale = cls.locale_from_request(cls, request)
        return cls(string, locale)

    def string_from_request(self, request):
        string = request.GET['string']
        return str(string)
    
    def locale_from_request(self, request):
        locale = request.GET['locale']
        return locale

    def __str__(self):
        return "string: " + self.string + " locale: " + str(self.locale)

    def __eq__(self, compare):
        return (self.string == compare.string and 
                self.locale == compare.locale)

    def __iter__(self):
        for i in range(len(self.string)):
            if i == 0:
                yield self.string
            else:
                yield self.string[:-i]

