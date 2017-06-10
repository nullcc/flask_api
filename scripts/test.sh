#!/bin/sh

TYPE=$1

python data/clean_db.py
python data/seed_data.py

if [ $TYPE = "--api" ] ; then
    python test/api/test.py
elif [ $TYPE = "--model" ] ; then
    python test/model/test.py
elif [ $TYPE = "--all" ] ; then
    python test/api/test.py
    python test/model/test.py
else
    python test/api/test.py
    python test/model/test.py
fi
