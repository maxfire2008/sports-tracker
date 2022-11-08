#!/bin/pwsh
$env:FLASK_ENV="development"
py -3.10 -m flask run
