# Real-Time Crypto Price Alert Engine

> A production style backend API built with FastAPI that lets authenticated users set price threshold alerts on any CoinGecko listed cryptocurrency, with a Celery background worker polling prices and WebSocket push notifications delivered the moment a threshold is crossed.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/Worker-Celery-37814A?logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Broker-Redis-DC382D?logo=redis&logoColor=white)
![WebSocket](https://img.shields.io/badge/Realtime-WebSocket-010101?logo=websocket&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## About

A real time backend system for cryptocurrency price monitoring. Users register, authenticate with JWT tokens, and create price alerts tied to any CoinGecko-listed coin. A Celery beat worker polls the CoinGecko API on a regular interval, checks every active alert against the current price, and pushes an instant notification to the user's browser via WebSocket the moment their threshold is crossed. Alerts automatically deactivate after firing, matching the standard behavior seen in production alert systems.

Built to demonstrate real world async backend skills: background task scheduling, external API integration, persistent WebSocket connections, and secure multi-user data isolation.

---

## Features

- **User Registration & Login**: Secure account creation with `pwdlib` password hashing and JWT-based session tokens
- **Price Alert Creation**: Users set a coin ID and a specific price threshold; alerts are stored and tracked per user
- **Live CoinGecko Polling**: A Celery beat worker polls the CoinGecko API at a configurable interval, checking all active alerts on every cycle
- **WebSocket Push Notifications**: When a threshold is crossed, the server pushes an instant notification to the user's open browser session, no polling required on the client side
- **One-Shot Alert Logic**: Alerts automatically deactivate after firing once, preventing repeated notifications
- **User-Scoped Data**: Each user can only view and delete their own alerts; cross-user access returns 403 Forbidden
- **Environment Variable Security**: All secrets and connection strings loaded from `.env`; the app raises a `ValueError` at startup if any are missing

---

## Tech Stack

| Layer               | Technology                          |
| ------------------- | ----------------------------------- |
| Framework           | FastAPI                             |
| ORM                 | SQLAlchemy                          |
| Database            | PostgreSQL                          |
| Authentication      | JWT (`PyJWT`), OAuth2 Password Flow |
| Password Hashing    | `pwdlib[argon2]`                    |
| Data Validation     | Pydantic v2                         |
| Background Worker   | Celery                              |
| Message Broker      | Redis                               |
| External Price Data | CoinGecko API (`httpx`)             |
| Real Time Transport | WebSocket (FastAPI native)          |
| Config Management   | `python-dotenv`                     |

---

## API Endpoints

| Method   | Endpoint           | Auth Required | Description                                       |
| -------- | ------------------ | ------------- | ------------------------------------------------- |
| `POST`   | `/users/register`  | ❌             | Register a new user                               |
| `POST`   | `/users/login`     | ❌             | Login and receive a JWT access token              |
| `POST`   | `/alerts`          | ✅             | Create a new price alert for a coin               |
| `GET`    | `/alerts/{id}`     | ✅             | Retrieve a specific alert by ID                   |
| `DELETE` | `/alerts/{id}`     | ✅             | Delete a specific alert (owner only)              |
| `WS`     | `/ws/{user_id}`    | ✅             | Open a persistent WebSocket connection for alerts |

---

## Architecture

The project separates concerns across five focused modules:

```
app/
│
├── main.py                  # FastAPI app instance, all route handlers, table creation
│
├── auth/
│   └── auth.py              # JWT encoding/decoding, OAuth2 scheme, get_current_user dependency
│
├── database/
│   ├── database.py          # Engine, SessionLocal, Base, and get_db() dependency
│   ├── models.py            # SQLAlchemy ORM models (Users, Alerts)
│   ├── schemas.py           # Pydantic request/response schemas
│   └── crud.py              # All database operations (create, read, update, delete)
│
├── services/
│   └── coingecko.py         # httpx client for fetching live coin prices from CoinGecko
│
├── tasks/
│   └── tasks.py             # Celery beat task: polls prices, checks thresholds, triggers alerts
│
└── websocket/
    └── connections.py       # WebSocket connection manager: tracks active sessions, pushes notifications
```

- **`auth/auth.py`** handles all identity logic — JWT creation, decoding, and the `get_current_user` dependency injected into protected routes
- **`database/models.py`** defines a one-to-many relationship between `Users` and `Alerts`, with `is_active` and `alert_fired_at` tracking the alert lifecycle
- **`services/coingecko.py`** is a thin `httpx` wrapper that fetches the current price of any coin by ID kept separate so it can be tested and reused independently
- **`tasks/tasks.py`** runs on a Celery beat schedule, iterates over all active alerts, fetches prices, and fires notifications via the WebSocket manager when thresholds are crossed
- **`websocket/connections.py`** maintains a registry of open WebSocket connections keyed by `user_id`, enabling the Celery worker to push targeted notifications to the right session

---

## How It Works

```
User creates alert (coin + threshold)
        │
        ▼
Alert stored in PostgreSQL (is_active = True)
        │
        ▼
Celery beat worker polls CoinGecko every 60 seconds
        │
        ▼
Current price compared against all active alerts
        │
   Threshold crossed?
        │
       YES
        │
        ▼
WebSocket pushes notification to user's browser
Alert marked is_active = False, alert_fired_at = timestamp
```

---

## Security

- Passwords hashed with `pwdlib[argon2]` plaintext passwords are never stored
- JWT tokens include `sub`, `exp`, and `action` claims; expired or tampered tokens return 401
- `SECRET_KEY`, `DATABASE_URL`, and `REDIS_URL` loaded from environment variables the app raises `ValueError` at startup if any are missing
- Ownership checks on all alert routes prevent users from accessing or deleting each other's data

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Dev-Umisol/Real-Time-Crypto-Price-Alert-Engine.git
cd Real-Time-Crypto-Price-Alert-Engine

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create a .env file with the following values
DATABASE_URL=postgresql://username:password@localhost:5432/real-time-price-alert
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379/0

# Generate a secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE \"real-time-price-alert\";"

# Start Redis (Docker recommended)
docker run -d -p 6379:6379 --name redis redis

# Run the API
uvicorn app.main:app --reload

# In a separate terminal — start the Celery worker
# Note: --pool=solo required on Windows
celery -A app.tasks.tasks worker --loglevel=info --pool=solo

# In a separate terminal — start the Celery beat scheduler
celery -A app.tasks.tasks beat --loglevel=info
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Future Improvements

- [ ] Add support for multiple alert types — percentage change alerts in addition to fixed price thresholds
- [ ] Add a `GET /alerts` endpoint to return all alerts for the current user
- [ ] Persist WebSocket sessions so users receive missed notifications on reconnect
- [ ] Add token refresh endpoint to avoid requiring re-login every 30 minutes
- [ ] Containerize with Docker Compose to orchestrate FastAPI, PostgreSQL, Redis, and Celery together
- [ ] Deploy with a live URL for portfolio demonstration

---

*Solo backend project — applying FastAPI, Celery, Redis, WebSockets, and PostgreSQL in a production-style real-time architecture 🐍*
