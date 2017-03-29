from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from core.behaviors import Timestampable, Contributable, Editable, Ownable
from core.utils import tokenize_text

# The following set of imports and the create_auth_token are placed in this models.py because
# it is guaranteed that it will be imported by Django at startup, as suggested by the Django REST Framework
# docs.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Article(Ownable, models.Model):
    title = models.CharField(max_length=512, blank=True)
    url = models.CharField(max_length=512, blank=True)
    text = models.TextField()
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)

    def __str__(self):
       return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('webapp:article', kwargs={'slug': str(self.slug)})

    @property
    def preview(self):
        return str(self.text)[:50] + ' ...'

    def as_tokens(self):
        return tokenize_text(self.text)


class UserWord(Ownable, models.Model):
    word = models.CharField(blank=True, max_length=512)
    ease = models.CharField(blank=True, max_length=20)
    pinyin = models.CharField(blank=True, max_length=512)
    articles = models.ManyToManyField(Article)

    class Meta:
        unique_together = ('owner', 'word')

    def __str__(self):
        return self.word


class PublicWord(models.Model):
    word = models.CharField(blank=True, max_length=512)
    pinyin = models.CharField(blank=True, max_length=512)

    def __str__(self):
        return self.word


class PublicDefinition(Timestampable, models.Model):
    word = models.ForeignKey(PublicWord)
    definition = models.CharField(max_length=512)

    def __str__(self):
        return self.definition


class UserDefinition(Ownable, Timestampable, models.Model):
    word = models.ForeignKey(UserWord)
    definition = models.CharField(max_length=512)

    class Meta:
        unique_together = ("owner", "word", "definition")

    def __str__(self):
        return self.definition
