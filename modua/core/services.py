from newspaper import Article
from wordfencer.parser import ChineseParser
import bs4
import requests


def fetch_article(url, language):
    if url == '' or language == '':
        raise Exception("fetch_article requires a url and a language")
    a = Article(url, language=language)
    a.download()
    a.parse()
    if not a.title:
        r = requests.get(url)
        html = bs4.BeautifulSoup(r.text)
        title = str(html.text.title)
    else:
        title = a.title

    return title, a.text

def tokenize_text(text):
    p = ChineseParser()
    tokens = []
    for string in text.split():
        tokens += p.parse(string)

    return tokens
