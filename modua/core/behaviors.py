from django.db import models
from django.contrib.auth.models import User


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, null=True, editable=False)

    class Meta:
        abstract = True


class Contributable(models.Model):
    contributor = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_contributor', null=True)

    class Meta:
        abstract = True


class Editable(models.Model):
    editor = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_editor', null=True)

    class Meta:
        abstract = True


class Ownable(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, related_name='%(app_label)s_%(class)s_owner', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def set_user(self, username):
        self.owner = User.objects.get(username=username)
        self.save()
