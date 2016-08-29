#!/bin/bash

CREATEDB="CREATE DATABASE modua;"
sudo -u postgres bash -c "psql -c \"${CREATEDB}\""
