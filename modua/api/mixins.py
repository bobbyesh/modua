from .utils import is_delimited
from .models import Language


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
            return get_object_or_404(queryset, **filter)  # Lookup the object


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
