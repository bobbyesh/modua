import subprocess
import configparser
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Setups up database.'

    def handle(self, *args, **kwargs):
        self.dir = os.path.abspath(os.path.dirname(__file__))
        self.config_path = self.dir + '/config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

        if not self.user_already_set():
            print('user_already_set')
            self.set_user()

        self.create_database()
            

    def set_user(self):
        subprocess.call(['bash', self.dir + '/createuser.sh'])

        self.config['DATABASE']['modua_user_set'] = '1'
        with open(self.config_path, 'w') as f:
            self.config.write(f)
        

    def user_already_set(self):
        return (
            'DATABASE' in self.config and
            'modua_user_set' in self.config['DATABASE'] and
            self.config['DATABASE']['modua_user_set'] == '1'
        )
            
    def create_database(self):
        path = self.dir + '/createdb.sh'
        subprocess.call(['bash', path])
