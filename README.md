
# URL Shortener

A URL shortener built with:

- Django
- DRF
- PostgreSQL
- Redis
- Docker Compose
- Celery

## Run

create an `.env` and then:  

```
docker compose up --build
```

## Migrations

```
docker compose exec web python manage.py migrate
```

## Create superuser

```
docker compose exec web python manage.py createsuperuser
```

## Performance Test
Modify ```redirect_load.js``` and then:
``` 
docker compose run --rm k6 run /app/tests/performance/redirect_load.js
```


## Architecture

```
User Request
    ↓
Django
    ↓
Redis Cache
    ↓
PostgreSQL
```