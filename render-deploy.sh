set -e 

poetry install --no-root
poetry lock --no-update
poetry run flask --app src.app db upgrade
poetry run gunicorn src.wsgi:app