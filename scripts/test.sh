#!/bin/sh

TYPE=$1

if [ $TYPE = "--api" ] ; then
    cd test/api
    python test.py
elif [ $TYPE = "--model" ] ; then
    cd test/model
    python test.py
elif [ $TYPE = "--all" ] ; then
    cd test/api
    python test.py

    cd ../../test/model
    python test.py
fi