from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from core.behaviors import Timestampable, Contributable, Editable, Ownable
from wordfencer.parser import ChineseParser

# The following set of imports and the create_auth_token are placed in this models.py because
# it is guaranteed that it will be imported by Django at startup, as suggested by the Django REST Framework
# docs.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Placed here so that loading occurs before view call (I think)
parser = ChineseParser()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Article(Ownable, models.Model):
    title = models.CharField(max_length=512)
    url = models.CharField(max_length=512, blank=True)
    body = models.TextField()
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
        return str(self.body)[:50] + ' ...'

    def as_tokens(self):
        return parser.parse(self.body)


class UserWord(Ownable, models.Model):
    word = models.CharField(max_length=100)
    ease = models.IntegerField(default=0)
    articles = models.ManyToManyField(Article)

    class Meta:
        unique_together = ('owner', 'word')

    def __str__(self):
        return self.word


class UserDefinition(Ownable, models.Model):
    word = models.ForeignKey(UserWord)
    definition = models.CharField(max_length=512)
    pinyin = models.CharField(max_length=512, blank=False)

    class Meta:
        unique_together = ('owner', 'word', 'definition',)

    def __str__(self):
        return self.definition


class PublicWord(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word


class PublicDefinition(models.Model):
    word = models.ForeignKey(PublicWord)
    definition = models.CharField(max_length=512)
    pinyin = models.CharField(max_length=512, blank=False)

    def __str__(self):
        return self.definition
