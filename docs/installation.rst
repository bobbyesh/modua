Project Installation (For Developers)
=====================================

Follow these directions in order if you are starting from scratch.  Some database dependencies are in the
requirements.txt, so install those first, and only then move onto the database setup.


Dependcies and Database Installation and Setup
==============================================

::

$ sudo apt-get install postgresql postgresql-contrib
$ sudo apt-get install libpq-dev python-dev python3-dev
$ sudo pip3 install -r requirements.txt
$ python3 manage.py createdb
$ python3 manage.py makemigrations api
$ python3 manage.py migrate


Run 'python3 manage.py runserver' to make sure there are no dependency or permission errors.

Installation is done.


.. NOTE:
    `python3 manage.py createdb` will create the database and create the user/password used by MODUA's specs.


Database Tasks
==============

Many database tasks have been scripted.  Below are the scripts and their usages.


Resetting the Database
----------------------

Sometimes you might want to delete your current database.  Type these commands::

$ python3 manage.py dropdb
$ python3 manage.py createdb
$ rm -r api/migrations
$ python3 manage.py makemigrations api
$ python3 manage.py migrate

Populate Database With Sample Data
----------------------------------

.. DANGER::

    (DEPRECATED)

::

$ python3 manage.py load_examples


Removing Language and Definition Model Instances from Database
--------------------------------------------------------------

.. DANGER::

    (DEPRECATED)
    
::

$ python3 manage.py delete_entries
