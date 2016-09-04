from django.core.exceptions import ObjectDoesNotExist
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
        return self.target

    @property
    def target(self):
        ''' Sets self.target to the Language model instance according to the url
        keyword `target`.

        '''
        if not hasattr(self, '_target'):
            try:
                self._target = Language.objects.get(
                    language=self.request.query_params['target']
                )
            except ObjectDoesNotExist:
                self._target = None

        return self._target

    @property
    def language(self):
        ''' Sets self.language to the Language model instance according to the url
        keyword `language`.

        '''
        if not hasattr(self, '_language'):
            query = self.get_language()
            try:
                self._language = Language.objects.get(language=query)
            except ObjectDoesNotExist:
                self._language = None

        return self._language

    @property
    def delimited(self):
        if not hasattr(self, '_is_delimited'):
            self._is_delimited = is_delimited(self.language)
        return self._is_delimited

    def get_language(self):
        if 'language' in self.kwargs:
            return self.kwargs['language']

        return self.request.data['language']
