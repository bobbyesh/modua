from rest_framework import serializers
from .models import PublicDefinition, PublicWord, UserDefinition, UserWord


class TokenSerializer(serializers.Serializer):
    string = serializers.CharField(trim_whitespace=True)


class PublicWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicWord
        fields = ('word', 'id')
        depth = 1


class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWord
        fields = ('word', 'ease', 'id')
        depth = 1


class PublicDefinitionSerializer(serializers.ModelSerializer):
    word = PublicWordSerializer()

    class Meta:
        model = PublicDefinition
        fields = ('word', 'definition', 'id')
        depth = 1


class UserDefinitionSerializer(serializers.ModelSerializer):
    word = UserWordSerializer()

    class Meta:
        model = UserDefinition
        fields = ('word', 'definition', 'id')
        depth = 1
