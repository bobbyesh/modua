import random
from django.core.management.base import BaseCommand
from api.models import Word

class Command(BaseCommand):
    help = 'Populates DB with CEDICT for Mandarin Chinese'

    def handle(self, *args, **kwargs):
        words = [str(w) for w in Word.objects.all()[:100]] + ['，', '。', '\n']
        string = ''.join(random.choice(words) for _ in range(100))
        print(string)
