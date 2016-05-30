from rest_framework import serializers
from .models import Definitions


class DefinitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definitions
        fields = ('word_character', 'definition', 'transliteration')
