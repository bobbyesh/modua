from django.db import models
from django.contrib.auth.models import User
from extras import CharNullField



class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_add_now=True, null=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, null=True, editable=False)

    class Meta:
        abstract = True


class Authorable(models.Model):
    author = models.ForeignKey(User, related_name='authors', null=True)

    class Meta:
        abstract = True


class Editable(models.Model):
    editor = models.ForeignKey(User, related_name='editors', null=True)

    class Meta:
        abstract = True
