# flagops

## Installation
```sh
$ pip3 install poetry
$ poetry install
$ poetry shell
```

## For running the server in development mode
```sh
$ uvicorn src.api.main:app --host 0.0.0.0 --port 8003 --reload
```

## For checking if server is running:
```sh
$ curl http://localhost:8003
$ curl http://localhost:8003/buildinfo
```

## Get all feature flags
```sh
$ curl http://localhost:8003/admin/featureflags -H "X-Tenant-Id: 6e58d992-1069-46d4-bc10-b79cab5716ea"
$ curl http://localhost:8003/admin/tagtypes -H "X-Tenant-Id: 6e58d992-1069-46d4-bc10-b79cab5716ea"
$ curl http://localhost:8003/admin/environments -H "X-Tenant-Id: 6e58d992-1069-46d4-bc10-b79cab5716ea"
```

## Create feature flag
```sh
$ curl -X POST -H "Content-Type: application/json" -H "X-Tenant-Id: 6e58d992-1069-46d4-bc10-b79cab5716ea" -d '{"name": "Tag Type 1"}' http://localhost:8003/admin/tagtypes
$ curl -X POST -H "Content-Type: application/json" -H "X-Tenant-Id: 6e58d992-1069-46d4-bc10-b79cab5716ea" -d '{"name": "Development"}' http://localhost:8003/admin/environments
$ curl -X POST -H "Content-Type: application/json" -H "X-Tenant-Id: 6e58d992-1069-46d4-bc10-b79cab5716ea" -d '{"name":"Flag 3","tags":[{"tag_type":"3c35f3d3-29da-4fa0-b8da-9d6c13c785fd","value":"foo"}]}' http://localhost:8003/admin/featureflags
```

## Testing setup
In order to run tests, we have to manually create the test database first:
```sh
$ sudo apt-get install postgresql-client
$ psql -h localhost -p 5432 -U flagopsuser -d postgres
CREATE DATABASE flagops_test_db;
CREATE USER flagops_test_user WITH PASSWORD 'flagops_test_password' CREATEDB;
ALTER ROLE flagops_test_user SET client_encoding TO 'utf8';
ALTER ROLE flagops_test_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE flagops_test_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE flagops_test_db TO flagops_test_user;
\q
```