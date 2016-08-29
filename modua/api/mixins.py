from core.utils import is_delimited
from .models import Language


class LanguageFilterMixin(object):
    '''
    Use for views that require identifying a single language from the
    `language` or `target` url keyword.

    Provides the language and delimited properties automatically.
    '''

    def get_language(self):
        return self.language

    def get_target(self):
        return self.language

    @property
    def target(self):
        if not hasattr(self, '_target'):
            self._target = Language.objects.get(
                language=self.request.query_params['target']
            )
        return self._target

    @property
    def language(self):
        if not hasattr(self, '_language'):
            self._language = Language.objects.get(
                    language=self.kwargs['language']
            )
        return self._language

    @property
    def delimited(self):
        if not hasattr(self, '_is_delimited'):
            self._is_delimited = is_delimited(self.language)
        return self._is_delimited
