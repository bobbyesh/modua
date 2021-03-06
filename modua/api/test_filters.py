from django.test import TestCase
from api.filters import PublicWordFilter, UserWordDataFilter, PublicDefinitionFilter, DefinitionFilter
from api.models import Word, UserWordData, PublicDefinition, Definition
from django.contrib.auth.models import User

class FilterTestMixin(object):

    def setUp(self):
        create_fields = self.field_vals
        if 'api:username' in create_fields:
            user = User.objects.create_user(username=create_fields.pop('api:username'))
            create_fields['owner'] = user

        if self.model == PublicDefinition:
            word = Word.objects.create(word=create_fields.pop('word'))
            create_fields['word'] = word
        elif self.model == Definition:
            word = UserWordData.objects.create(word=create_fields.pop('word'))
            create_fields['word'] = word

        try:
            self.model.objects.create(**create_fields)
        except Exception as e:
            name = type(self).__name__
            raise Exception("Failure in creating model instance in {}".format(name))


    def test_fields(self):
        for field, val in self.field_vals.items():
            filter = self.get_filter()
            filtered = filter({field: val}, queryset=self.get_queryset())
            self.assertEqual(
                list(self.get_queryset()),
                list(filtered),
                "The filter field {} did not produce expected results".format(field)
            )

    def get_queryset(self):
        return self.model.objects.all()

    def get_filter(self):
        return self.filter


class PublicWordFilterTestCase(FilterTestMixin, TestCase):
    model = Word
    filter = PublicWordFilter
    field_vals = {'word': 'foo', 'pinyin': 'phauew'}


class UserWordFilterTestCase(FilterTestMixin, TestCase):
    model = UserWordData
    filter = UserWordDataFilter
    field_vals = {
        'word': 'foo',
        'pinyin': 'phauew',
        'api:username': 'john',
        'ease': 'easy',
    }


class PublicDefinitionFilterTestCase(FilterTestMixin, TestCase):
    model = PublicDefinition
    filter = PublicDefinitionFilter
    field_vals = {
        'word': 'foo',
        'definition': 'somedefinition',
    }


class UserDefinitionFilterTestCase(FilterTestMixin, TestCase):
    model = Definition
    filter = DefinitionFilter
    field_vals = {
        'api:username': 'john',
        'word': 'foo',
        'definition': 'somedefinition',
    }
