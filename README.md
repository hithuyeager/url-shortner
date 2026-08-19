# URL Shortener API

A basic URL shortener REST API built with **FastAPI** and **PostgreSQL** (via `asyncpg`). It lets you submit a long URL and get back a short one, then redirects anyone who visits the short URL to the original destination.

## Features

- `POST /shorten` — accepts a long URL and returns a shortened URL
- `GET /{short_code}` — redirects to the original long URL
- Async database access using a connection pool (`asyncpg`)
- Clean separation of concerns: routes → services → repositories → database

## Project Structure

```
url-shortner-main/
├── main.py                   # FastAPI app entrypoint, sets up DB pool lifespan
├── config.py                 # Loads settings (DATABASE_URL, BASE_URL) from .env
├── requirements.txt          # Python dependencies
├── .env.example               # Template for environment variables
├── api/
│   └── routes.py             # API endpoints (/shorten, /{short_code})
├── services/
│   └── url_services.py       # Business logic: short code generation, lookup
├── repositories/
│   └── url_repository.py     # Raw DB queries (insert, select)
├── schemas/
│   └── url.py                # Pydantic request/response models
└── db/
    ├── database.py           # Creates the asyncpg connection pool
    └── schema.sql            # SQL to create the `urls` table
```

## How It Works

1. A client sends a `POST /shorten` request with a JSON body containing `original_url`.
2. The service layer generates a random 8-character alphanumeric short code (using Python's `secrets` module for security) and retries up to 10 times on the rare chance of a collision.
3. The short code and original URL are stored in the PostgreSQL `urls` table.
4. The API responds with the full short URL (`BASE_URL` + short code).
5. When someone visits `GET /{short_code}`, the API looks up the original URL in the database and issues a `307 Temporary Redirect` to it. If the code doesn't exist, it returns a `404`.

## Prerequisites

- Python 3.10+
- PostgreSQL running locally or accessible remotely
- `pip` for installing dependencies

## Setup & Running Locally

### 1. Clone / unzip the project
Navigate into the project folder:
```bash
cd url-shortner-main
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the database
Create a PostgreSQL database, then run the schema:
```bash
psql -U <your_user> -d <your_database> -f db/schema.sql
```

### 5. Configure environment variables
Copy the example file and fill in your values:
```bash
cp .env.example .env
```
Edit `.env`:
```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<database>
BASE_URL=http://localhost:8000
```

### 6. Run the server
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`.

## API Usage

### Shorten a URL
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.example.com/some/very/long/path"}'
```
**Response:**
```json
{
  "short_url": "http://localhost:8000/aB3xY9kD"
}
```

### Use the short URL
Visiting the returned `short_url` in a browser (or via `curl -L`) will redirect you to the original URL:
```bash
curl -L http://localhost:8000/aB3xY9kD
```

## Tech Stack

- **FastAPI** — web framework
- **asyncpg** — async PostgreSQL driver
- **Pydantic / pydantic-settings** — request validation and config management
- **Uvicorn** — ASGI server