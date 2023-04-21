#!/usr/bin/env bash
# exit on error
set -o errexit

# poetry install
<<<<<<< HEAD
pip install -r requirements.txt
=======
# pip install -r requirements.txt
>>>>>>> 032cede (modificado build.hs)



python manage.py collectstatic --no-input
python manage.py migrate
