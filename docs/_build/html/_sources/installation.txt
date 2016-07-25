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
#. sudo apt-get install libpq-dev python-dev
#. sudo pip3 install -r modua/modua/requirements.txt
#. sudo su - postgres
#. createdb modua
#. createuser -P root_webbuild
    ..note:  Type 'happytime3.14' when prompted for the password (omit quotes)
#. psql
#. GRANT ALL PRIVILEGES ON DATABASE modua TO root_webbuild;
#. ALTER USER root_webbuild CREATEDB;

Run 'python3 manage.py test' and make sure the tests run.  Don't mind if they fail or pass, just that there
are no dependency or permission errors when the test_modua database is created.

Installation is done.
