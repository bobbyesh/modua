from rest_framework import serializers
from .models import Definitions, Languages

class DefinitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definitions
        fields = ('word_character', 'definition', 'transliteration')



class LanguagesWordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ('language', 'words')
    

class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ('language',)
