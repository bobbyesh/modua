from rest_framework import serializers
from .models import Definition, Language


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('word', 'definition', 'transliteration')


class LanguageWordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('language', 'word')


class LanguageSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name = 'definition-list',
        lookup_field = 'language',
    )

    class Meta:
        model = Language
        fields = ('language', 'url')
