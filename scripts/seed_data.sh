#!/bin/sh

cd data
python clean_db.py
python seed_data.py