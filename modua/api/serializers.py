from rest_framework import serializers
from .models import PublicDefinition, Language, PublicWord, UserDefinition, UserWord


class TokenSerializer(serializers.Serializer):
    string = serializers.CharField(trim_whitespace=True)
    position = serializers.IntegerField()


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('language', 'id')


class PublicWordSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = PublicWord
        fields = ('word', 'language', 'id')
        depth = 1


class UserWordSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()

    class Meta:
        model = UserWord
        fields = ('word', 'language', 'ease', 'id')
        depth = 1


class PublicDefinitionSerializer(serializers.ModelSerializer):

    word = PublicWordSerializer()
    language = LanguageSerializer()

    class Meta:
        model = PublicDefinition
        fields = ('word', 'definition', 'language', 'id')
        depth = 1


class UserDefinitionSerializer(serializers.ModelSerializer):

    word = UserWordSerializer()
    language = LanguageSerializer()

    class Meta:
        model = UserDefinition
        fields = ('word', 'definition', 'language', 'id')
        depth = 1


