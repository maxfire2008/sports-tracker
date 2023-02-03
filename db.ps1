#!/bin/pwsh
docker run -i -e POSTGRES_PASSWORD=postgres -p 5431:5432 postgres
