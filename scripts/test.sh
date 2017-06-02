#!/bin/sh

TYPE=$1

if [ $TYPE = "--e2e" ] ; then
    cd tests/e2e
    python test.py
elif [ $TYPE = "--unit" ] ; then
    cd tests/unit
    python test.py
elif [ $TYPE = "--all" ] ; then
    cd tests/e2e
    python test.py

    cd ../../tests/unit
    python test.py
fi