# CMS Interface

Designing and developing a backend system to interact with Center for Medicare
and Medicaid Services (CMS) using the Blue Button 2.0 API.

## Requirements

1. Python (3.10.4)
2. Pip (22.0.4)
3. Postgres (Docker 14.2)

## Database

Starting docker postgres

```
docker run --name cms-wrapper-postgres \
    -e POSTGRES_USER=cms \
    -e POSTGRES_PASSWORD=cms \
    -e POSTGRES_DB=cms \
    -p 5432:5432 \
    -v $(pwd)/data/postgres:/var/lib/postgresql/data \
    -d postgres:14.2
```
