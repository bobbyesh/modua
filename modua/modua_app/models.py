from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from extras import CharNullField

'''These models are currently only for testing.'''


class Languages(models.Model):
    pk_languages_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_user_added_lang_id = models.ForeignKey(User, related_name='fk_user_added_lang_id', null=True)
    fk_user_updated_lang_id = models.ForeignKey(User, related_name='fk_user_updated_lang_id', null=True)
    #TODO: Create fulltext index in DB
    language = models.CharField(null=True, max_length=150)
    alphabet = models.CharField(null=True, max_length=300)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_languages_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Languages, self).save()

    def __str__(self):
        return self.language

class Dictionary_Apis(models.Model):
    pk_dictionary_apis_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_user_added_dic_id = models.ForeignKey(User, related_name='fk_user_added_dic_id', null=True)
    fk_user_updated_dic_id = models.ForeignKey(User, related_name='fk_user_updated_dic_id', null=True)
    # TODO: Create fulltext index in DB
    api_name = models.CharField(null=True, max_length=150)
    # This should be Usage, notes, and known issues
    api_description = CharNullField(null=True, max_length=8000, blank=True)
    api_type = models.CharField(null=True, max_length=150)
    # Actual site of the dictionary we want to use, not the URL from connecting to it
    api_site = models.CharField(null=True, max_length=2000)
    # URL used if it's that's how we need to connect to the API
    api_base_url = models.CharField(null=True, max_length=2000)
    # The API key if you need to register an application with the site - may not be necessary
    api_key = models.CharField(null=True, max_length=500)
    # The key needed/issued to access the API - may not be necessary
    api_id_key = models.CharField(null=True, max_length=500)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_dictionary_apis_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Dictionary_Apis, self).save()

    def __str__(self):
        return self.api_name


class Word_Types(models.Model):
    pk_word_types_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_user_added_word_id = models.ForeignKey(User, related_name='fk_user_added_word_id', null=True)
    fk_user_updated_word_id = models.ForeignKey(User, related_name='fk_user_updated_word_id', null=True)
    word_type = models.CharField(null=True, max_length=150)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_word_types_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Word_Types, self).save()

    def __str__(self):
        return self.word_type


class Definitions(models.Model):
    pk_definition_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_sourcelang_id = models.ForeignKey(Languages, related_name='fk_sourcelang_id', null=True)
    fk_definitionlang_id = models.ForeignKey(Languages, related_name='fk_definitionlang_id', null=True)
    fk_dictionary_apis_id = models.ForeignKey(Dictionary_Apis, related_name='fk_dictionary_apis_id', null=True)
    fk_user_contributor_id = models.ForeignKey(User, related_name='fk_user_contributor_id', null=True)
    fk_word_type_id = models.ForeignKey(Word_Types, related_name='fk_word_type_id', null=True)
    # TODO: Create fulltext index in DB
    definition = models.CharField(null=True, max_length=8000)
    transliteration = CharNullField(null=True, max_length=8000, blank=True)
    total_lookups = models.IntegerField(null=True)
    user_added = models.IntegerField(null=True)
    archived = models.BooleanField(default=False, null=False)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)
    archived_date = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_definition_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Definitions, self).save()

    def __str__(self):
        return self.definition


class Country(models.Model):
    pk_country_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_user_added_country_id = models.ForeignKey(User, related_name='fk_user_added_country_id', null=True)
    fk_user_updated_country_id = models.ForeignKey(User, related_name='fk_user_updated_country_id', null=True)
    country_name = models.CharField(null=True, max_length=250)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_country_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Country, self).save()

    def __str__(self):
        return self.country_name


class Region(models.Model):
    pk_region_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_country_region_id = models.ForeignKey(Country, related_name='fk_country_region_id', null=True)
    fk_user_added_region_id = models.ForeignKey(User, related_name='fk_user_added_region_id', null=True)
    fk_user_updated_region_id = models.ForeignKey(User, related_name='fk_user_updated_region_id', null=True)
    region = models.CharField(null=True, max_length=300)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_region_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Region, self).save()

    def __str__(self):
        return self.region


class City(models.Model):
    pk_city_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_country_city_id = models.ForeignKey(Country, related_name='fk_country_city_id', null=True)
    fk_region_city_id = models.ForeignKey(Region, related_name='fk_region_city_id', null=True)
    fk_user_added_city_id = models.ForeignKey(User, related_name='fk_user_added_city_id', null=True)
    fk_user_updated_city_id = models.ForeignKey(User, related_name='fk_user_updated_city_id', null=True)
    city_name = models.CharField(null=True, max_length=150)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_city_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(City, self).save()

    def __str__(self):
        return self.city_name


class User_Definitions(models.Model):
    pk_user_definitions_id = models.AutoField(null=False, primary_key=True, editable=False)
    fk_user_owner_id = models.ForeignKey(User, related_name='fk_user_owner_id', null=True)
    fk_definitions_id = models.ForeignKey(Definitions, related_name='fk_definitions_id', null=True)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.pk_user_definitions_id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(User_Definitions, self).save()
