import cedict
import django
from django.conf import settings

settings.configure(
    SECRET_KEY='_437(1odgxoxv2yz3cle&9-$h)!9z5i7^^h=2kd#li)ycb&o2f',
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'modua.modua_app',
        'modua',
        'twitter_bootstrap',
    ],
    # WSGI_APPLICATION='modua.wsgi.application',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'modua',
            'USER': 'root_webbuild',
            'PASSWORD': 'happytime3.14',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
)
django.setup()

# This import has to be here because you can't import the models before django has setup
# I mean, it seems to be the case.
from modua.modua_app.models import Definitions

# Verify that this is your filename
CEDICT_FILE = "cedict_1_0_ts_utf-8_mdbg.txt"


# This cleans the data by escaping the apostrophes
def clean_entry(def_boi):
    return_string = str(def_boi)
    return_string = return_string.replace("'", "\'")
    return return_string


def store_def_boi(word, trans, def_arr):
    try:
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
            store_this_guy = Definitions(word=word, transliteration=trans, definition=definition)
            store_this_guy.save()
            print("Definition: {0} | {1} | {2} | {3}".format(store_this_guy.pk_definition_id, store_this_guy.word,
                                                             store_this_guy.transliteration, store_this_guy.definition))
    except Exception as e:
        error_file = open("cedict_error.txt", "a+")
        error_file.writelines("{0} | {1} | {2} | {3}\n".format(e, word, trans, def_arr))


def import_dictionary(file_name):
    infile = open(file_name)
    for ch_trad, ch_simp, trans, defs, variants, mw in cedict.iter_cedict(infile):
        # If the traditional and the simple are the same then only insert one
        if ch_trad == ch_simp:
            store_def_boi(ch_trad, trans, defs)
        else:
            store_def_boi(ch_trad, trans, defs)
            store_def_boi(ch_simp, trans, defs)

    infile.close()


import_dictionary(CEDICT_FILE)
