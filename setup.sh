#!/bin/bash

echo "Installing PostgreSQL and set up server"
sudo apt-get install postgresql postgresql-client postgresql-contrib
service postgresql start
chmod +x ./scriptpostgres.sh
sudo -u postgres ./scriptpostgres.sh
echo "Installing requirements"
pip install -r requirements.txt
