#! /usr/bin/env bash
FILE=/app/app/config/app.db
if test -f "$FILE";
then
    echo "$FILE exists."
else
    python3 setup.py
    echo "ran setup"
fi
