#cedict_import.py
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from tqdm import tqdm
from api.models import PublicDefinition, PublicWord
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
    for definition in def_arr:
        try:
            word_obj, created = PublicWord.objects.get_or_create(word=word, pinyin=trans, defaults={'word': word, 'pinyin': trans})
            PublicDefinition.objects.create(word=word_obj, definition=definition)
        except IntegrityError as e:
            print(e)


def import_dictionary(file_name):
    cnt = 0
    with open(file_name) as f:
        for idx, line in enumerate(f):
            cnt = idx

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
