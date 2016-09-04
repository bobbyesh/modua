# mixins.py

from api.models import Word
from api.mixins import LanguageFilterMixin
from core.utils import is_punctuation
from collections import defaultdict

class UserMixin(LanguageFilterMixin):

    def get_counts(self, text):
        counts = defaultdict(int)
        if not hasattr(self, 'tokens'):
            self.get_tokens(text)
        else:
            for item in self.tokens:
                if hasattr(item, 'ease') and str(item.ease) in counts:
                    counts[str(item.ease)] += 1
        return counts


    def get_tokens(self, text):
        self.tokens = []
        for token in tokenize_text(text):
            if is_punctuation(token):
                word = token
            else:
                word = Word.objects.filter(word=token, language=self.language, users__user=self.request.user)
                if word:
                    assert len(word) == 1
                    word = word[0]
                else:
                    try:
                        word = Word.objects.get(word=token, language=self.language)
                    except ObjectDoesNotExist:
                        word = token

            tokens.append(word)

        return self.tokens

