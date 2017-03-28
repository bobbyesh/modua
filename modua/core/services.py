from newspaper import Article
from wordfencer.parser import ChineseParser
import bs4
import requests


def fetch_article(url, language):
    a = Article(url, language=language)
    a.download()
    a.parse()
    title = a.title
    text = a.text
    if not title:
        r = requests.get(url)
        html = bs4.BeautifulSoup(r.content)
        title = html.find('h1').text

    return title, text
