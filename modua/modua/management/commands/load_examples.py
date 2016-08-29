from django.core.management.base import BaseCommand
from api.models import Definition, Language


class Command(BaseCommand):

    help = 'Setups up database.'

    def handle(self, *args, **kwargs):
        english = Language.objects.create(language='en')
        chinese = Language.objects.create(language='zh')
        for translation, word in [('你好', 'hello'), ('音响', 'speakers'),('天气', 'weather')]:
            Definition.objects.create(language=english, word=word, target=chinese, translation=translation)
