# URL Shortener

A production-oriented URL shortener built for learning scalable backend and system design concepts.

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- ClickHouse
- Redis
- RabbitMQ
- JWT Authentication
- Docker Compose

---

# Features

- Short URL generation
- Fast redirect endpoint
- JWT authentication
- User-owned links
- Asynchronous click processing
- Analytics dashboard
- Time-series analytics
- Top links
- Unique visitor counting
- Dockerized development environment

---

# Run

Create an `.env` file and then run:

```bash
docker compose up --build
```

---

# Database Migrations

PostgreSQL:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

ClickHouse tables are initialized automatically from:

```
analytics/schema/001_create_tables.sql
```

---

# Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

# Performance Test

Modify `redirect_load.js` and run:

```bash
docker compose run --rm k6 run /app/tests/performance/redirect_load.js
```

---

# Architecture

```
                          +----------------------+
                          |        Client        |
                          +----------+-----------+
                                     |
                                     v
                          +----------------------+
                          |     Django / DRF     |
                          +----------+-----------+
                                     |
                +--------------------+--------------------+
                |                                         |
                |                                         |
                v                                         v
      +---------------------+                  +----------------------+
      |       Redis         |                  |     PostgreSQL       |
      |  Redirect Cache     |                  |  ShortURL            |
      +---------------------+                  |  LinkOwnership       |
                                               |  Users              |
                                               +----------+----------+
                                                          |
                                                          |
                           publish click event            |
                           (RabbitMQ fanout)             |
                                                          |
                                                          v
                                              +----------------------+
                                              |      RabbitMQ        |
                                              +----------+-----------+
                                                         |
                                                         |
                                                         v
                                            +-------------------------+
                                            | Analytics Consumer      |
                                            +-----------+-------------+
                                                        |
                                                        |
                                                        v
                                              +----------------------+
                                              |     ClickHouse       |
                                              |    click_events      |
                                              +----------+-----------+
                                                         |
                                                         |
                                            analytics queries
                                                         |
                                                         v
                                              +----------------------+
                                              | Analytics API        |
                                              | Dashboard            |
                                              | Top Links            |
                                              | Time Series          |
                                              +----------------------+
```

---

# Data Storage

## PostgreSQL (OLTP)

Stores transactional application data.

### Tables

- User
- ShortURL
- LinkOwnership

Used for:

- Authentication
- URL lookup
- Ownership
- Fast point lookups

---

## Redis

Used as a cache for redirect lookups to reduce PostgreSQL load.

---

## RabbitMQ

Decouples redirects from analytics.

Every redirect publishes a click event asynchronously.

---

## ClickHouse (OLAP)

Stores click events for analytical workloads.

Example columns:

- owner_id
- short_code
- original_url
- created_at
- ip_address
- user_agent
- referrer



# Request Flow

## Redirect

```
Client
   │
   ▼
Django
   │
   ├── Redis lookup
   │
   ├── PostgreSQL fallback
   │
   ├── Redirect response
   │
   └── Publish click event
            │
            ▼
        RabbitMQ
            │
            ▼
   Analytics Consumer
            │
            ▼
       ClickHouse
```

---

## Analytics

```
Client
   │
   ▼
Django
   │
   ├── PostgreSQL
   │      └── owned links
   │
   └── ClickHouse
          ├── dashboard
          ├── top links
          ├── time series
          └── unique visitors
```

---


# Future Improvements

- Kafka instead of RabbitMQ
- Batch inserts into ClickHouse
- Materialized Views
- Dead Letter Queue
- Distributed ClickHouse cluster
- Rate limiting
- Link expiration
- Custom aliases
- QR code generation
- Prometheus + Grafana monitoring
- CI/CD pipeline