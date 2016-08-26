from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from extras import CharNullField


class Language(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    user_added = models.ForeignKey(User, related_name='user_added_lang', null=True)
    user_updated = models.ForeignKey(User, related_name='user_updated_lang', null=True)
    #TODO: Create fulltext index in DB
    language = models.CharField(null=True, max_length=150)
    script = models.CharField(null=True, max_length=300)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Language, self).save()

    def __str__(self):
        return '%s' % self.language


class DictionaryAPI(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    user_added = models.ForeignKey(User, related_name='user_added_dictionary_api', null=True)
    user_updated = models.ForeignKey(User, related_name='user_updated_dictionary_api', null=True)
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
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(DictionaryAPI, self).save()

    def __str__(self):
        return self.api_name


class WordType(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    user_added = models.ForeignKey(User, related_name='user_added_wordtype', null=True)
    user_updated = models.ForeignKey(User, related_name='user_updated_wordtype', null=True)
    word_type = models.CharField(null=True, max_length=150)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(WordType, self).save()

    def __str__(self):
        return self.word_type


class Definition(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    language = models.ForeignKey(Language, related_name='current_lang', null=True)
    target = models.ForeignKey(Language, related_name='target_lang', null=True)
    dictionary_apis = models.ForeignKey(DictionaryAPI, related_name='dictionary_apis', null=True)
    user_contributor = models.ForeignKey(User, related_name='user_contributor', null=True)
    word_type = models.ForeignKey(WordType, related_name='word_type_id', null=True)
    # TODO: Create fulltext index in DB
    word = CharNullField(null=True, max_length=600, blank=True)
    definition = models.CharField(null=True, max_length=8000)
    transliteration = CharNullField(null=True, max_length=8000, blank=True)
    total_lookups = models.IntegerField(null=True)
    user_added = models.IntegerField(null=True)
    archived = models.BooleanField(default=False, null=False)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)
    archived_date = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Definition, self).save()

    def __str__(self):
        return '%s' % self.word


class Country(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    user_added = models.ForeignKey(User, related_name='user_added_country', null=True)
    user_updated = models.ForeignKey(User, related_name='user_updated_country', null=True)
    country_name = models.CharField(null=True, max_length=250)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Country, self).save()

    def __str__(self):
        return self.country_name


class Region(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    country_region = models.ForeignKey(Country, related_name='country_region', null=True)
    user_added = models.ForeignKey(User, related_name='user_added_region', null=True)
    user_updated = models.ForeignKey(User, related_name='user_updated_region', null=True)
    region = models.CharField(null=True, max_length=300)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(Region, self).save()

    def __str__(self):
        return self.region


class City(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    country_city = models.ForeignKey(Country, related_name='country_city', null=True)
    region_city = models.ForeignKey(Region, related_name='region_city', null=True)
    user_added = models.ForeignKey(User, related_name='user_added_city', null=True)
    user_updated = models.ForeignKey(User, related_name='user_updated_city', null=True)
    city_name = models.CharField(null=True, max_length=150)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(City, self).save()

    def __str__(self):
        return self.city_name


class UserDefinition(models.Model):
    id = models.AutoField(null=False, primary_key=True, editable=False)
    user_owner = models.ForeignKey(User, related_name='user_owner', null=True)
    definitions = models.ForeignKey(Definition, related_name='definitions', null=True)
    added = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self):
        if not self.id:
            self.added = timezone.now()
        self.updated = timezone.now()
        super(UserDefinition, self).save()
