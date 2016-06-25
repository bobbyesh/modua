from rest_framework import serializers
from .models import Definitions, Languages


class DefinitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definitions
        fields = ('word_character', 'definition', 'transliteration')

class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ('language',)
