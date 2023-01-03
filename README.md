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

