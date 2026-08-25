# Digital Alpha - Transactions Dashboard

A full-stack transaction analytics dashboard built as part of the Digital Alpha assessment.

The application provides a centralized interface to monitor transactions, analyze spending patterns, explore payment activity, inspect individual transactions, and redeem rewards using earned coins.

---

## Project Overview

The Digital Alpha Transactions Dashboard is designed to provide a clear view of transaction activity and spending behavior.

The dashboard includes:

- Transaction monitoring
- Transaction search and filtering
- Server-side pagination
- Transaction sorting
- Transaction details
- Spending analytics
- Payment method analytics
- Top merchant analysis
- Monthly spending trends
- Interactive charts
- Rewards and coin redemption

The application uses a React frontend connected to a FastAPI REST API backed by PostgreSQL.

---

## Key Features

### 1. Transaction Dashboard

The transaction dashboard provides a paginated view of transaction records.

Supported functionality:

- View total transactions
- View total transaction amount
- View successful transactions
- View failed transactions
- View pending transactions
- Search transactions by merchant
- Filter transactions by category
- Filter transactions by status
- Filter transactions by payment method
- Filter transactions by date range
- Filter transactions by minimum amount
- Filter transactions by maximum amount
- Combine multiple filters
- Sort transactions by ID
- Sort transactions by date
- Sort transactions by amount
- Sort transactions by merchant
- Sort ascending or descending
- Open individual transaction details

### 2. Spending Analytics

The dashboard provides visual analytics based on transaction data.

#### Spending by Category

Shows transaction spending across categories such as:

- Groceries
- Education
- Insurance
- Shopping
- Travel
- Health
- Fuel
- Utilities
- Entertainment
- Food & Dining

Category chart interactions can be used to filter the transaction table.

#### Payment Methods

Provides a breakdown of transaction activity by payment method:

- Credit Card
- Debit Card
- Netbanking
- UPI

Payment method chart interactions can be used to filter transactions.

#### Monthly Spending Trend

The dashboard includes a monthly spending trend showing spending over time.

The monthly analytics are calculated from successful transactions stored in PostgreSQL.

#### Top Merchants

The dashboard displays the top merchants ranked by transaction activity and spending amount.

---

## Rewards

The application includes a rewards system based on earned transaction coins.

Users can:

- View available coins
- View the reward catalogue
- View reward costs
- Redeem available rewards
- Validate available coin balance
- Track redeemed coins
- View remaining coin balance

The backend validates the available balance before allowing a redemption.

---

# Technology Stack

## Frontend

- React
- Vite
- JavaScript
- CSS
- Recharts

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

## Database

- PostgreSQL

## Development Tools

- Git
- GitHub
- npm
- Python virtual environment

---

# Architecture

The application follows a simple full-stack architecture:

```text
React + Vite
      |
      | REST API
      v
   FastAPI
      |
      | SQLAlchemy
      v
 PostgreSQL
```

### Frontend

The React frontend is responsible for:

- Dashboard interface
- Transaction filters
- Sorting
- Pagination
- Interactive charts
- Transaction detail interactions
- Rewards interface
- Loading and error states

### Backend

The FastAPI backend is responsible for:

- REST API endpoints
- Request validation
- Transaction queries
- Filtering
- Sorting
- Pagination
- Analytics
- Transaction details
- Reward validation
- Reward redemption
- Database operations

### Database

PostgreSQL is used as the persistent relational database.

SQLAlchemy is used as the database access layer.

---

# Project Structure

```text
digital-alpha-assessment/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── transaction.py
│   │   ├── schemas.py
│   │   ├── summary_schemas.py
│   │   ├── reward.py
│   │   └── reward_schemas.py
│   │
│   ├── data/
│   ├── scripts/
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   └── ...
│   │
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── AI-USAGE.md
├── ASSUMPTIONS.md
├── DECISIONS.md
└── README.md
```

---

# API

## Health Check

```http
GET /health
```

Returns the API health status.

Example:

```json
{
  "status": "ok"
}
```

---

## Transaction APIs

### Get Transactions

```http
GET /api/transactions
```

Returns a paginated list of transactions.

### Supported Query Parameters

- `page`
- `page_size`
- `search`
- `category`
- `status`
- `payment_method`
- `date_from`
- `date_to`
- `min_amount`
- `max_amount`
- `sort_by`
- `sort_order`

### Example

```http
GET /api/transactions?page=1&page_size=20
```

### Category Filter

```http
GET /api/transactions?category=Groceries
```

### Status Filter

```http
GET /api/transactions?status=SUCCESS
```

### Payment Method Filter

```http
GET /api/transactions?payment_method=UPI
```

### Amount Range Filter

```http
GET /api/transactions?min_amount=1000&max_amount=5000
```

### Date Range Filter

```http
GET /api/transactions?date_from=2026-01-01&date_to=2026-06-30
```

Multiple filters can be combined.

---

## Get Transaction Details

```http
GET /api/transactions/{transaction_id}
```

Returns details for a specific transaction.

Example:

```http
GET /api/transactions/10001
```

---

## Transaction Summary

```http
GET /api/transactions/summary
```

Returns dashboard analytics including:

- Total transactions
- Total amount
- Successful transactions
- Failed transactions
- Pending transactions
- Spending by category
- Payment method breakdown
- Top merchants
- Monthly spending trend

---

# Rewards API

## Get Rewards

```http
GET /api/rewards
```

Returns the active reward catalogue.

## Get Reward Balance

```http
GET /api/rewards/balance
```

Returns:

- Available coins
- Earned coins
- Redeemed coins

## Redeem Reward

```http
POST /api/rewards/redeem
```

Redeems a reward after validating the available coin balance.

---

# Running the Project Locally

## Prerequisites

Make sure the following are installed:

- Python 3
- Node.js
- npm
- PostgreSQL
- Git

---

## Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the PostgreSQL database connection according to the project's database configuration.

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the URL provided by Vite, typically:

```text
http://localhost:5173
```

---

## Production Build

To create a production build:

```bash
cd frontend
npm run build
```

The production files are generated in:

```text
frontend/dist/
```

---

# Data and Analytics

The dashboard analytics are calculated from transaction data stored in PostgreSQL.

The system calculates:

- Transaction totals
- Transaction status counts
- Category spending
- Payment method distribution
- Merchant activity
- Monthly spending

Analytics are generated from the database rather than being hard-coded into the frontend.

---

# Filtering and Pagination

Transaction filtering is handled through the backend API.

Supported filters include:

- Merchant
- Category
- Status
- Payment method
- Date range
- Minimum amount
- Maximum amount

Multiple filters can be combined.

Transactions are paginated on the server to avoid loading the complete dataset into the browser at once.

---

# Sorting

Supported sorting fields:

- Transaction ID
- Date
- Amount
- Merchant

Supported directions:

- Ascending
- Descending

---

# Error Handling

The backend validates:

- Invalid date ranges
- Invalid amount ranges
- Invalid sorting fields
- Invalid sorting directions
- Missing transactions
- Missing rewards
- Insufficient reward coin balances

The frontend provides loading and error states for API operations.

---

# Documentation

Additional implementation documentation is included in the repository.

### AI-USAGE.md

Documents AI-assisted development used during the project.

### ASSUMPTIONS.md

Documents product and implementation assumptions made where the assessment requirements were not completely explicit.

### DECISIONS.md

Documents important technical and architectural decisions, including:

- React + Vite
- FastAPI
- PostgreSQL
- SQLAlchemy
- Server-side pagination
- Combined filtering
- Sorting
- Analytics
- Rewards
- API separation

---

# Engineering Highlights

- Full-stack React + FastAPI architecture
- PostgreSQL-backed transaction data
- REST API design
- Server-side pagination
- Combined transaction filters
- Date and amount range filtering
- Controlled sorting
- Transaction detail API
- Category spending analytics
- Payment method analytics
- Top merchant analytics
- Monthly spending trend
- Interactive chart filtering
- Reward balance validation
- Reward redemption
- Backend business-rule validation
- Loading and error handling

---

# Assessment Scope

The implementation focuses on transaction monitoring, spending analytics, transaction filtering, transaction details, and rewards functionality required by the assessment.

The following areas are outside the current assessment scope:

- Authentication
- Multi-user authorization
- Real payment processing
- External reward-provider integrations
- Real-time transaction streaming

---

# Author

**Abhishek Karri**

B.Tech - Electronics & Communication Engineering  
National Institute of Technology Durgapur

GitHub:  
https://github.com/Abhishek-NIT-btech