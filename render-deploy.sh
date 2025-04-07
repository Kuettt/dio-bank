
#! /usr/bin/env bash

set -e 

rm -rf migrations/
poetry run flask --app src.app db init
poetry run flask --app src.app db migrate -m "recriando tudo"
poetry run flask --app src.app db upgrade



