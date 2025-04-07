
#! /usr/bin/env bash

set -e 

poetry install --no-root

poetry run flask --app src.app db init 
poetry run flask --app src.app db migrate -m "remake"
poetry run flask --app src.app db upgrade 
poetry run gunicorn src.wsgi:app

