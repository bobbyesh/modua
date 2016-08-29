from django.core.management.base import BaseCommand
from api.models import Definition, Language


class Command(BaseCommand):

    help = 'Setups up database.'

    def handle(self, *args, **kwargs):
        english = Language.objects.create(language='en', delimited=True)
        chinese = Language.objects.create(language='zh',delimited=False)
        for translation, word in [('你好', 'hello'), ('音响', 'speakers'),('天气', 'weather')]:
            Definition.objects.create(language=english, word=word, target=chinese, translation=translation)

        for word, translation in [('你好', 'hello'), ('音响', 'speakers'),('天气', 'weather')]:
            Definition.objects.create(language=chinese, word=word, target=english, translation=translation)

        Definition.objects.create(
            language=chinese,
            target=english,
            word='我',
            translation='I',
        )
        Definition.objects.create(
            language=chinese,
            target=english,
            word='是',
            translation='am',
        )
        Definition.objects.create(
            language=chinese,
            target=english,
            word='是',
            translation='is',
        )
        Definition.objects.create(
            language=chinese,
            target=english,
            word='美国',
            translation='America',
        )
        Definition.objects.create(
            language=chinese,
            target=english,
            word='人',
            translation='person',
        )
