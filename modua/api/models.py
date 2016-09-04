from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from core.behaviors import Timestampable, Contributable, Editable, Ownable


class Language(Contributable, Editable, Timestampable, models.Model):
    language = models.CharField(blank=True, max_length=150)
    script = models.CharField(blank=True, max_length=300)
    delimited = models.BooleanField(default=True)

    def __str__(self):
        return self.language


class DictionaryAPI(Timestampable, models.Model):
    """

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

    """

    name = models.CharField(blank=True, max_length=150)
    description = models.CharField(blank=True, max_length=8000)
    api_type = models.CharField(blank=True, max_length=150)
    site = models.CharField(blank=True, max_length=2000)
    base_url = models.CharField(blank=True, max_length=2000)
    api_key = models.CharField(blank=True, max_length=500)
    id_key = models.CharField(blank=True, max_length=500)
    language = models.ForeignKey(Language, related_name='apis', null=True)

    def __str__(self):
        return str(self.api_name)


class WordType(Contributable, Editable, Timestampable, models.Model):
    word_type = models.CharField(blank=True, max_length=150)

    def __str__(self):
        return self.word_type


class Article(Ownable, models.Model):
    title = models.CharField(max_length=2000, blank=True)
    url = models.CharField(max_length=2000, blank=True)
    text = models.TextField(blank=False)
    language = models.ForeignKey(Language, related_name='api_article_language')
    slug = models.SlugField(max_length=40, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': str(self.slug)})

    @property
    def preview(self):
        return str(self.text)[:50] + ' ...'


class Word(Ownable, models.Model):
    word = models.CharField(blank=True, max_length=600)
    users = models.ManyToManyField(User)
    ease = models.CharField(blank=True, max_length=20)
    language = models.ForeignKey(Language)
    transliteration = models.CharField(blank=True, max_length=8000)
    article = models.ManyToManyField(Article)

    def __str__(self):
        return self.word

    @classmethod
    def create(cls, word, language, definition, definition_language, ease='', transliteration=''):
        l, created = Language.objects.get_or_create(language=language)
        definition_l, created = Language.objects.get_or_create(language=definition_language)
        word_instance =  cls(word=word, language=l, ease=ease, transliteration=transliteration)
        word_instance.save()
        Definition.objects.get_or_create(word=word_instance, language=definition_l, definition=definition)
        return word_instance

    def add_definition(self, language, definition):
        query_instance, created = Language.objects.get_or_create(language=language)
        Definition.objects.get_or_create(word=self, language=query_instance, definition=definition)

    def set_language(self, language, delimited=True):
        language, created = Language.objects.get_or_create(language=language, delimited=delimited)
        self.language = language
        self.save()


class Definition(Timestampable, Contributable, models.Model):
    word = models.ForeignKey(Word)
    definition = models.CharField(max_length=8000)
    language = models.ForeignKey(Language)
    word_type = models.ForeignKey(WordType, related_name='word_type_id', null=True)

    def __str__(self):
        return self.translation


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
