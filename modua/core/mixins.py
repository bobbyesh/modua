# mixins.py

from api.models import Word, Article
from core.utils import is_punctuation, tokenize_text
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist

class ArticleMixin(object):

    def get_article_context(self, user):
        '''Returns a tuple of (tokens, counts).  `tokens` is the Word model instances with ratings, and `counts` is a dictionary containing counts of words
        in each easiness rating.


        To access the `easy` count in the template, use the following variables:: 

            {{ counts.easy }}
            {{ counts.hard }}
            {{ counts.new }}
            {{ counts.unknown }}

        '''
        self.set_text()
        return self.get_tokens(user), self.get_counts()

    def set_text(self):
        slug = self.kwargs['slug']
        self.article = Article.objects.get(slug=slug)
        self.language = self.article.language
        self.text = self.article.text
        return self.text

    def get_counts(self):
        counts = defaultdict(int)
        if not hasattr(self, 'tokens'):
            self.get_tokens()
        else:
            for item in self.tokens:
                if hasattr(item, 'ease'):
                    counts[str(item.ease)] += 1
        return counts


    def get_tokens(self, user):
        '''Returns a list of elements that are either `api.models.Word` instances or just strings.

        If the user has not saved a particular token as a word before, then that word is
        get or created with an `ease` of `new`, but it is not associated with that user via the 
        ManyToMany `users` field in the :model:`Word`.

        '''
        if hasattr(self, 'tokens'):
            return self.tokens
        if not hasattr(self, 'text'):
            self.set_text()

        self.tokens = []
        for token in tokenize_text(self.text):
            if is_punctuation(token):
                word = token
            else:
                word = Word.objects.filter(word=token, language=self.language, users__username=user.username)
                if word:
                    assert len(word) == 1
                    word = word[0]
                else:
                    word, created = Word.objects.get_or_create(word=token, language=self.language, ease='new')

            self.tokens.append(word)

        return self.tokens
