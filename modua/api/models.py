from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.behaviors import Timestampable
from extras import CharNullField


class Language(Authorable, Editable, Timestampable, models.Model):
    '''

    .. TODO: Create fulltext index in DB

    '''
    id = models.AutoField(null=False, primary_key=True, editable=False)
    language = models.CharField(null=True, max_length=150)
    script = models.CharField(null=True, max_length=300)

    def __str__(self):
        return '%s' % self.language


class DictionaryAPI(Authorable, Editable, Timestampable, models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    # TODO: Create fulltext index in DB
    name = models.CharField(null=True, max_length=150)
    # This should be Usage, notes, and known issues
    description = CharNullField(null=True, max_length=8000, blank=True)
    api_type = models.CharField(null=True, max_length=150)
    # Actual site of the dictionary we want to use, not the URL from connecting to it
    site = models.CharField(null=True, max_length=2000)
    # URL used if it's that's how we need to connect to the API
    base_url = models.CharField(null=True, max_length=2000)
    # The API key if you need to register an application with the site - may not be necessary
    api_key = models.CharField(null=True, max_length=500)
    # The key needed/issued to access the API - may not be necessary
    id_key = models.CharField(null=True, max_length=500)

    def __str__(self):
        return self.api_name


class WordType(Authorable, Editable, Timestampable, models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    word_type = models.CharField(null=True, max_length=150)

    def __str__(self):
        return self.word_type


class Definition(Timestampable, models.Model):
    '''

    ..TODO  Create fulltext index in DB

    '''
    id = models.AutoField(null=False, primary_key=True, editable=False)
    language = models.ForeignKey(Language, related_name='current_lang', null=True)
    target = models.ForeignKey(Language, related_name='target_lang', null=True)
    dictionary_apis = models.ForeignKey(DictionaryAPI, related_name='dictionary_apis', null=True)
    user_contributor = models.ForeignKey(User, related_name='user_contributor', null=True)
    word_type = models.ForeignKey(WordType, related_name='word_type_id', null=True)
    word = CharNullField(null=True, max_length=600, blank=True)
    definition = models.CharField(null=True, max_length=8000)
    transliteration = CharNullField(null=True, max_length=8000, blank=True)
    total_lookups = models.IntegerField(null=True)
    user_added = models.IntegerField(null=True)
    archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return '%s' % self.word


class Country(Authorable, Editable, Timestampable, models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    country_name = models.CharField(null=True, max_length=250)

    def __str__(self):
        return self.country_name


class Region(Authorable, Editable, Timestampable, models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    country_region = models.ForeignKey(Country, related_name='country_region', null=True)
    region = models.CharField(null=True, max_length=300)

    def __str__(self):
        return self.region


class City(Authorable, Editable, Timestampable, models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    country_city = models.ForeignKey(Country, related_name='country_city', null=True)
    region_city = models.ForeignKey(Region, related_name='region_city', null=True)
    city_name = models.CharField(null=True, max_length=150)

    def __str__(self):
        return self.city_name


class UserDefinition(Timestampable, models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    user_owner = models.ForeignKey(User, related_name='user_owner', null=True)
    definitions = models.ForeignKey(Definition, related_name='definitions', null=True)
