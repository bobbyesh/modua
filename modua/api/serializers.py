from rest_framework import serializers
from .models import Definition, Language, Word

class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = ('word', 'language', 'ease', 'id')
        depth = 1

class DefinitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Definition
        fields = ('word', 'definition', 'id')
        depth = 2


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('language', 'id')
