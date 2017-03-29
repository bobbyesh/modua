from django.test import TestCase
from api.filters import PublicWordFilter, UserWordFilter, PublicDefinitionFilter, UserDefinitionFilter
from api.models import PublicWord, UserWord, PublicDefinition, UserDefinition
from django.contrib.auth.models import User

class FilterTestMixin(object):

    def setUp(self):
        create_fields = self.field_vals
        if 'username' in create_fields:
            user = User.objects.create_user(username=create_fields.pop('username'))
            create_fields['owner'] = user

        if self.model == PublicDefinition:
            word = PublicWord.objects.create(word=create_fields.pop('word'))
            create_fields['word'] = word
        elif self.model == UserDefinition:
            word = UserWord.objects.create(word=create_fields.pop('word'))
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
    model = PublicWord
    filter = PublicWordFilter
    field_vals = {'word': 'foo', 'pinyin': 'phauew'}


class UserWordFilterTestCase(FilterTestMixin, TestCase):
    model = UserWord
    filter = UserWordFilter
    field_vals = {
        'word': 'foo',
        'pinyin': 'phauew',
        'username': 'john',
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
    model = UserDefinition
    filter = UserDefinitionFilter
    field_vals = {
        'username': 'john',
        'word': 'foo',
        'definition': 'somedefinition',
    }
