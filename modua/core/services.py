from newspaper import Article
from wordfencer.parser import ChineseParser


def fetch_article(url, language):
    if url == '' or language == '':
        raise Exception("fetch_article requires a url and a language")
    a = Article(url, language=language)
    a.download()
    a.parse()
    return a.title, a.text

def tokenize_text(text):
    p = ChineseParser()
    tokens = []
    for string in text.split():
        tokens += p.parse(string)

    return tokens
