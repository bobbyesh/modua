from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.behaviors import Timestampable, Authorable, Editable
from core.fields import CharNullField


class Definition(Timestampable, models.Model):
    '''

    ..TODO  Create fulltext index in DB

    '''
    language = models.ForeignKey(Language, related_name='language', null=True)
    target = models.ForeignKey(Language, related_name='target_lang', null=True)
    api = models.ForeignKey(DictionaryAPI, related_name='apis', null=True)
    contributor = models.ForeignKey(User, related_name='contributor', null=True)
    word_type = models.ForeignKey(WordType, related_name='word_type_id', null=True)
    word = CharField(blank=True, max_length=600)
    definition = models.CharField(max_length=8000)
    transliteration = CharField(blank=True, max_length=8000)
    total_lookups = models.IntegerField(null=True)
    user_added = models.IntegerField(null=True)
    archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return '%s' % self.word


class Language(Authorable, Editable, Timestampable, models.Model):
    '''

    .. TODO: Create fulltext index in DB


    '''

    language = models.CharField(blank=True, max_length=150)
    script = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return self.language


class DictionaryAPI(Authorable, Editable, Timestampable, models.Model):
    '''

    .. TODO: Create fulltext index in DB

    :Fields:
        `description`:
            This should be Usage, notes, and known issues.

        `site`:
            Actual site of the dictionary we want to use, not the URL
            from connecting to it.

        `base_url`:
            URL used if it's that's how we need to connect to the API.

        `api_key`:
            The API key if you need to register an application with the site - may not
            be necessary.

        `id_key`:
            The key needed/issued to access the API - may not be necessary.

    '''
    name = models.CharField(blank=True, max_length=150)
    description = CharField(blank=True, max_length=8000)
    api_type = models.CharField(blank=True, max_length=150)
    site = models.CharField(blank=True, max_length=2000)
    base_url = models.CharField(blank=True, max_length=2000)
    api_key = models.CharField(blank=True, max_length=500)
    id_key = models.CharField(blank=True, max_length=500)

    def __str__(self):
        return str(self.api_name)


class WordType(Authorable, Editable, Timestampable, models.Model):
    word_type = models.CharField(blank=True, max_length=150)

    def __str__(self):
        return self.word_type


class Country(Authorable, Editable, Timestampable, models.Model):
    country = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return self.country_name


class Region(Authorable, Editable, Timestampable, models.Model):
    country = models.ForeignKey(Country, related_name='country', null=True)
    region = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return self.region


class City(Authorable, Editable, Timestampable, models.Model):
    country_city = models.ForeignKey(Country, related_name='country_city', null=True)
    region_city = models.ForeignKey(Region, related_name='region_city', null=True)
    city_name = models.CharField(blank=True, max_length=150)

    def __str__(self):
        return self.city_name


class UserDefinition(Timestampable, models.Model):
    user = models.ForeignKey(User, related_name='user', null=True)
    definitions = models.ForeignKey(Definition, related_name='definitions', null=True)
