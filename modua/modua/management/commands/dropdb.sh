#!/bin/bash

DROPDB="DROP DATABASE modua;"
sudo -u postgres bash -c "psql -c \"${DROPDB}\""
