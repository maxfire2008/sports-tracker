#!/bin/pwsh
$env:FLASK_ENV="development"
$env:FLASK_APP="sports_tracker"
py -3.10 -m flask run
