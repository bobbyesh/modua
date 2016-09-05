from rest_framework import serializers
from .models import Definition, Language, Word

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('language', 'id')

class WordSerializer(serializers.ModelSerializer):

    language = LanguageSerializer()

    class Meta:
        model = Word
        fields = ('word', 'language', 'ease', 'id')
        depth = 1


class DefinitionSerializer(serializers.ModelSerializer):

    word = WordSerializer()

    class Meta:
        model = Definition
        fields = ('word', 'definition', 'id')
        depth = 1


