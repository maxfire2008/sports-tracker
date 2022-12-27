#!/bin/pwsh
docker run -e POSTGRES_PASSWORD=postgres -p 5431:5432 postgres
