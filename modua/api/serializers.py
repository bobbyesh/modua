from rest_framework import serializers
from .models import Word, Definition, UserWordData


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('word', 'id')
        depth = 1


class UserWordDataSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    word = WordSerializer()

    class Meta:
        model = UserWordData
        fields = ('word', 'ease', 'id', 'owner')
        depth = 1


class DefinitionSerializer(serializers.ModelSerializer):
    word = UserWordDataSerializer()

    class Meta:
        model = Definition
        fields = ('word', 'definition', 'id', 'pinyin',)
        depth = 1

