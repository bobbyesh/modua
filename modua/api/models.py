from django.db import models
from django.contrib.auth.models import User
from core.behaviors import Timestampable, Contributable, Editable


class DictionaryAPI(Timestampable, models.Model):
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
    description = models.CharField(blank=True, max_length=8000)
    api_type = models.CharField(blank=True, max_length=150)
    site = models.CharField(blank=True, max_length=2000)
    base_url = models.CharField(blank=True, max_length=2000)
    api_key = models.CharField(blank=True, max_length=500)
    id_key = models.CharField(blank=True, max_length=500)

    def __str__(self):
        return str(self.api_name)


class WordType(Contributable, Editable, Timestampable, models.Model):
    word_type = models.CharField(blank=True, max_length=150)

    def __str__(self):
        return self.word_type


class Language(Contributable, Editable, Timestampable, models.Model):
    '''

    .. TODO: Create fulltext index in DB


    '''

    language = models.CharField(blank=True, max_length=150)
    script = models.CharField(blank=True, max_length=300)
    delimited = models.BooleanField(default=True)

    def __str__(self):
        return self.language


class Context(models.Model):
    text = models.TextField(blank=True)


class Definition(Timestampable, Contributable, models.Model):
    '''

    ..TODO  Create fulltext index in DB

    '''

    word = models.CharField(blank=True, max_length=600)
    translation = models.CharField(max_length=8000)
    language = models.ForeignKey(Language, related_name='source_language')
    target = models.ForeignKey(Language, related_name='target_language')
    transliteration = models.CharField(blank=True, max_length=8000)
    word_type = models.ForeignKey(WordType, related_name='word_type_id', null=True)
    context = models.ForeignKey(Context, related_name='context_definitions', null=True)

    api = models.ForeignKey(DictionaryAPI, related_name='apis', null=True)
    total_lookups = models.IntegerField(null=True)
    user_added = models.IntegerField(null=True)
    archived = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.word


class Country(Contributable, Editable, Timestampable, models.Model):
    country = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return self.country_name


class Region(Contributable, Editable, Timestampable, models.Model):
    country = models.ForeignKey(Country, related_name='country_region', null=True)
    region = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return self.region


class City(Contributable, Editable, Timestampable, models.Model):
    country_city = models.ForeignKey(Country, related_name='country_city', null=True)
    region_city = models.ForeignKey(Region, related_name='region_city', null=True)
    city_name = models.CharField(blank=True, max_length=150)

    def __str__(self):
        return self.city_name


class UserDefinition(Timestampable, models.Model):
    user = models.ForeignKey(User, related_name='user', null=True)
    definitions = models.ForeignKey(Definition, related_name='definitions', null=True)
