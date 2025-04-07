
#! /usr/bin/env bash

set -e 

rm -rf migrations/
poetry run flask db init
poetry run flask db migrate -m "recriando tudo"
poetry run flask db upgrade



