#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r gcsbackend/requirements.txt

# optional: run migrations if your production DB is reachable during build
# python gcsbackend/manage.py migrate --noinput

python gcsbackend/manage.py collectstatic --noinput
