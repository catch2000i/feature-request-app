#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

service mysql restart

echo "sleeping 1 sec..."
sleep 1

# preparing test database and data
python3.6 sqlalchemy_declarative.py
python3.6 sqlalchemy_insert.py

python3.6 /app/app.py
