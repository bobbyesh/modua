from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from core.behaviors import Timestampable, Contributable, Editable, Ownable


''' The following set of imports and the create_auth_token are placed in this models.py because
it is guaranted that it will be imported by Django at startup, as suggest by the Django REST Framework
docs.
'''
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Language(Contributable, Editable, Timestampable, models.Model):
    language = models.CharField(blank=True, max_length=150)
    script = models.CharField(blank=True, max_length=300)
    delimited = models.BooleanField(default=True)

    def __str__(self):
        return self.language


class Article(Ownable, models.Model):
    title = models.CharField(max_length=512, blank=True)
    url = models.CharField(max_length=512, blank=True)
    text = models.TextField()
    language = models.ForeignKey(Language, related_name='api_article_language')
    slug = models.SlugField(max_length=200, allow_unicode=True)

    def __str__(self):
       return self.slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': str(self.slug)})

    @property
    def preview(self):
        return str(self.text)[:50] + ' ...'


class UserWord(Ownable, models.Model):
    word = models.CharField(blank=True, max_length=512)
    ease = models.CharField(blank=True, max_length=20)
    language = models.ForeignKey(Language)
    transliteration = models.CharField(blank=True, max_length=512)
    articles = models.ManyToManyField(Article)

    class Meta:
        unique_together = ('owner', 'word')

    def __str__(self):
        return self.word


class PublicWord(models.Model):
    word = models.CharField(blank=True, max_length=512)
    language = models.ForeignKey(Language)
    transliteration = models.CharField(blank=True, max_length=512)

    def __str__(self):
        return self.word


class PublicDefinition(Timestampable, models.Model):
    word = models.ForeignKey(PublicWord)
    definition = models.CharField(max_length=512)
    language = models.ForeignKey(Language)

    def __str__(self):
        return self.definition


class UserDefinition(Ownable, Timestampable, models.Model):
    word = models.ForeignKey(UserWord)
    definition = models.CharField(max_length=512)
    language = models.ForeignKey(Language)

    class Meta:
        unique_together = ("owner", "word", "definition", "language")

    def __str__(self):
        return self.definition


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
    description = models.CharField(blank=True, max_length=512)
    api_type = models.CharField(blank=True, max_length=150)
    site = models.CharField(blank=True, max_length=2000)
    base_url = models.CharField(blank=True, max_length=512)
    api_key = models.CharField(blank=True, max_length=512)
    id_key = models.CharField(blank=True, max_length=512)
    language = models.ForeignKey(Language, related_name='apis', null=True)

    def __str__(self):
        return self.name


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
