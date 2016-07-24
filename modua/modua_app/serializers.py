from rest_framework import serializers
from .models import Definitions, Languages


class DefinitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definitions
        fields = ('word', 'definition', 'transliteration')


class LanguagesWordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ('language', 'word')


class LanguagesSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name = 'definition-list',
        lookup_field = 'language',
    )

    class Meta:
        model = Languages
        fields = ('language', 'url')
