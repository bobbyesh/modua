#cedict_import.py
from django.core.management.base import BaseCommand
from tqdm import tqdm
from api.models import PublicDefinition, Language, PublicWord
from . import cedict_parser


# This cleans the data by escaping the apostrophes
def clean_entry(def_boi):
     return_string = str(def_boi)
     return_string = return_string.replace("'", "\'")
     return return_string


def store_def_boi(word, trans, def_arr):
    # Escape the apostrophe going into the DB
    word = clean_entry(word)
    trans = clean_entry(trans)

    def_idx = 0
    while def_idx < len(def_arr):
        def_arr[def_idx] = clean_entry(def_arr[def_idx])
        def_idx += 1

    # Do the insertion
    # If there is more than one definition insert them both as different rows
    zh, created = Language.objects.get_or_create(language='zh')
    en, created = Language.objects.get_or_create(language='en')
    for definition in def_arr:
        word_instance = PublicWord.objects.create(word=word, language=zh, transliteration=trans)
        definition_instance = PublicDefinition.objects.create(word=word_instance, definition=definition, language=en)


def import_dictionary(file_name):
    cnt = 0
    lines = []
    with open(file_name) as f:
        for cnt, line in enumerate(f):
            lines.append(line)

    # tqdm is the progress bar
    with tqdm(total=cnt) as pbar:
        with open(file_name) as infile:
            for ch_trad, ch_simp, trans, defs, variants, mw in cedict_parser.iter_cedict(infile):
                # If the traditional and the simple are the same then only insert one
                if ch_trad == ch_simp:
                    store_def_boi(ch_trad, trans, defs)
                else:
                    store_def_boi(ch_trad, trans, defs)
                    store_def_boi(ch_simp, trans, defs)
                pbar.update(1)

# Verify that this is your filename
CEDICT_FILE = "modua/data/cedict.txt"


class Command(BaseCommand):

    help = 'Populates DB with CEDICT for Mandarin Chinese'

    def handle(self, *args, **kwargs):
        import_dictionary(CEDICT_FILE)
