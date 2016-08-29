Project Installation (For Developers)
=====================================

Follow these directions in order if you are starting from scratch.  Some database dependencies are in the
requirements.txt, so install those first, and only then move onto the database setup.


Dependencies Installation
=========================

sudo pip3 install -r modua/modua/requirements.txt


Database Installation and Setup
===============================

#. sudo apt-get install postgresql postgresql-contrib
#. sudo apt-get install libpq-dev python-dev python3-dev
#. sudo pip3 install -r modua/modua/requirements.txt
#. python3 manage.py createdb
#. python3 manage.py makemigrations api
#. python3 manage.py migrate


Run 'python3 manage.py runserver' Make sure there are no dependency or permission errors.

Installation is done.


.. NOTE:
    `python3 manage.py createdb` will create the database and create the user/password used by MODUA's specs.


Resetting the Database
======================

Sometimes you might want to delete your current database.  To do so, type these commands:

#. python3 manage.py dropdb
#. python3 manage.py createdb
