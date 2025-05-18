### Development deployment

1. Fill up `.env` file (see [`env-example`](env-example))
2. Install `Poetry`
3. Install depenencies:
```shell
poetry install
```
4. Run bot:
```shell
poetry run python3 main.py
```

### Production deployment

1. Fill up `.env` file (see [`env-example`](env-example))
2. Build and run container:
```shell
docker compose build && docker compose up
```