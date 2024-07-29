#!/bin/bash

#gunicorn -b 0.0.0.0:5000 --workers=1 --reload main:app

if [ "$FLASK_ENV" == "development" ]; then
        python main.py
else
        gunicorn -b 0.0.0.0:5000 --workers=1 --preload main:app
fi