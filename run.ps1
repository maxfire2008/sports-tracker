#!/bin/pwsh
$env:FLASK_ENV="development"
$env:FLASK_APP="sports_tracker"

py -3.10 -m flask db init
py -3.10 -m flask db migrate
py -3.10 -m flask db upgrade

py -3.10 -m flask run
