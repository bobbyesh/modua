import subprocess
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Drops the modua database.'

    def handle(self, *args, **kwargs):
        answer = input("Are you sure you want to remove the MODUA database?(y/n)")
        if answer.lower() in {'yes', 'y'}:
            path = os.path.abspath(os.path.dirname(__file__)) + '/dropdb.sh'
            subprocess.call(['bash', path])
