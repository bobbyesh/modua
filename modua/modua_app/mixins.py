from .utils import is_delimited
from .models import Language

class LanguageFilterMixin(object):
    '''
    Use for views that require identifying a single language from the
    'language' url keyword.

    Provides the language and delimited properties automatically.
    '''

    @property
    def language(self):
        if not hasattr(self, '_language'):
            self._language = Language.objects.filter(
                    language=self.kwargs['language']
            )
        return self._language

    @property
    def delimited(self):
        if not hasattr(self, '_is_delimited'):
            self._is_delimited = is_delimited(self.language)
        return self._is_delimited
