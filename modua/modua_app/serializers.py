from modua.requirements. rest_framework import serializers
from .models import Definitions


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definitions
        fields = ('text', 'definition', 'language')
