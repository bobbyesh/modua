from django.core.management.base import BaseCommand
from api.models import Definition, Language


class Command(BaseCommand):

    help = 'Setups up database.'

    def handle(self, *args, **kwargs):
        Definition.objects.all().delete()
        Language.objects.all().delete()
