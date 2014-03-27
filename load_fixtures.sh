#!/bin/sh

python manage.py loaddata global_change_lab/fixtures/groups.json
python manage.py loaddata global_change_lab/fixtures/flatpages.json
