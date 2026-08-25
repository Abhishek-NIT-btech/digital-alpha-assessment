# Digital Alpha Assessment

A full-stack transaction dashboard built with React, Vite, FastAPI, and PostgreSQL.

## Features

- Transaction dashboard with summary statistics
- Transaction listing with pagination
- Search by merchant
- Filter by category
- Filter by transaction status
- Filter by payment method
- Sort transactions
- Backend API with validation
- SQLite-backed transaction data
- Responsive frontend interface

## Project Structure

```text
digital-alpha-assessment/
├── backend/
│   ├── app/
│   ├── data/
│   ├── scripts/
│   └── .gitignore
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Production Build

```bash
cd frontend
npm run build
```

## API Endpoints

```text
GET /health
GET /api/transactions
GET /api/transactions/summary
```

The transactions endpoint supports pagination, searching, filtering, and sorting.
