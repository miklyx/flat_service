
# Flat Service FastAPI

A FastAPI-based service for collecting Berlin flats information.

## Features

- Runs own telegram client to read data from channels
- Database integration with redis
- Puts "hot" data to redis, all data to Postgres
- Had endpoints to see statistics

## Installation

Create virtual environment, then:

```bash
pip install -r requirements.txt
```

## Usage

```bash
uvicorn main:app --reload
```

## Deployed to

https://flat-service-w52m.onrender.com/

/refresh_flats - refreshes flats
/flats - shows current flats

## API Documentation

Access the API documentation at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## License

MIT