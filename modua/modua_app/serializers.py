from rest_framework import serializers
from .models import Definition


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('text', 'definition', 'language')
