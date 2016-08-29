#!/bin/bash

Q1="CREATE USER root_webbuild WITH PASSWORD 'happytime3.14';"
Q2="GRANT ALL PRIVILEGES ON DATABASE modua TO root_webbuild;"
Q3="ALTER USER root_webbuild CREATEDB;"
SQL="${Q1}${Q2}${Q3}"
sudo -u postgres bash -c "psql -c \"${SQL}\""
