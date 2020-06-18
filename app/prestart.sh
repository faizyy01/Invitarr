#! /usr/bin/env bash
FILE=/app/app/config/app.db
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else
    python setup.py
fi
