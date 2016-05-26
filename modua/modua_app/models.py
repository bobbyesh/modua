from django.db import models

'''These models are currently only for testing.'''

class Definition(models.Model):
    text = models.CharField(max_length=20)
    definition = models.CharField(max_length=200)
    language = models.CharField(max_length=20)
