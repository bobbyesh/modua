from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PublicDefinition, PublicWord, UserDefinition, UserWord


class PublicWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicWord
        fields = ('word', 'id')
        depth = 1


class UserWordSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = UserWord
        fields = ('word', 'ease', 'id', 'owner')
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
        fields = ('word', 'definition', 'id', 'owner')
        depth = 1

