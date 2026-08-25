# Technical Decisions

This document explains the main technical and product decisions made for the Digital Alpha transaction dashboard.

## 1. React + Vite

The frontend uses React with Vite.

React provides component-based UI development and makes it straightforward to manage dashboard state such as filters, pagination, sorting, rewards, and transaction details.

Vite was selected for its fast development server and simple production build process.

## 2. FastAPI

FastAPI is used for the backend REST API.

It provides:

- Clear API route definitions
- Request validation
- Response schemas
- Automatic API documentation
- Good integration with SQLAlchemy

The backend is responsible for business rules and database operations.

## 3. PostgreSQL

PostgreSQL is used as the primary database.

The application originally supported local development with SQLite, but PostgreSQL was selected for the completed implementation because it provides a stronger relational database solution and is more appropriate for transaction-oriented data.

## 4. SQLAlchemy

SQLAlchemy is used as the database access layer.

Using an ORM keeps database queries organized around application models and makes the backend easier to maintain.

## 5. Server-Side Pagination

Transaction records are paginated by the backend rather than loading all 10,000 transactions into the browser at once.

This keeps API responses smaller and provides a scalable approach for larger datasets.

## 6. Combined Filtering

Transaction filters are designed to work together.

For example, a user can filter transactions by:

- Category
- Status
- Payment method
- Merchant
- Date range
- Amount range

The backend receives the active filters and returns the matching transaction set.

## 7. Sorting

Sorting is performed using explicit supported fields:

- Transaction ID
- Date
- Amount
- Merchant

The sort direction can be ascending or descending.

This keeps sorting predictable and avoids arbitrary database expressions from the client.

## 8. Transaction Details

Transaction rows are interactive.

Selecting a transaction opens a detail view instead of navigating to a separate page.

This keeps the user within the dashboard and makes it easier to inspect a transaction and return to the current filtered list.

## 9. Analytics

The dashboard provides analytics for:

- Spending by category
- Payment methods
- Top merchants
- Monthly spending

These analytics are calculated from the transaction data rather than using hard-coded frontend values.

## 10. Chart Interaction

Charts are interactive where useful.

Selecting an analytics value can be used to narrow the transaction table to the corresponding data.

This connects the visual analytics with the underlying transaction records rather than treating charts as static decoration.

## 11. Rewards

Rewards are implemented through backend endpoints and PostgreSQL-backed redemption records.

The backend validates the available coin balance before allowing redemption.

A successful redemption records the redemption and updates the effective available balance.

## 12. API Separation

The frontend does not directly access PostgreSQL.

The architecture is:

React frontend
→ FastAPI REST API
→ SQLAlchemy
→ PostgreSQL

This separation keeps database credentials and database logic on the server.

## 13. Error and Loading States

API operations include loading and error handling.

The UI should communicate when data is being loaded and when an API request cannot be completed instead of silently displaying incorrect values.

## 14. Scope

The implementation focuses on the requirements of the assessment.

Features such as authentication, multi-user authorization, real payment processing, external reward-provider integration, and real-time transaction streaming are outside the current scope unless explicitly required by the assessment.