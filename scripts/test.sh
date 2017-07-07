#!/bin/sh

TYPE=$1

python tests/data/clean_db.py
python tests/data/seed_data.py

if [ "$TYPE" = "--e2e" ] ; then
    python tests/test_e2e.py
elif [ "$TYPE" = "--unit" ] ; then
    python tests/test_unit.py
elif [ "$TYPE" = "--all" ] ; then
    python tests/test_e2e.py
    python tests/test_unit.py
else
    python tests/test_e2e.py
    python tests/test_unit.py
fi
