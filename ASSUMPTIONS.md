# Assumptions

This document records product and implementation assumptions made where the assessment requirements were not completely explicit.

## Transactions

- The transaction dataset is treated as the source of truth for dashboard statistics and analytics.
- Transaction amounts are displayed in Indian Rupees (₹).
- Transaction IDs are unique.
- Transaction dates are treated as the transaction timestamp.
- The dashboard uses server-side pagination for transaction listings.
- Filters can be combined rather than operating independently.
- Sorting is applied to the filtered transaction set.
- The default transaction page size is 20 records.

## Transaction Filters

The transaction table supports filtering by:

- Merchant
- Category
- Status
- Payment method
- Date range
- Minimum amount
- Maximum amount

Date filters are inclusive of the selected dates.

Amount filters are inclusive of the entered minimum and maximum values.

## Transaction Details

- Selecting a transaction opens its complete details without navigating away from the dashboard.
- The transaction detail view is presented as a modal/drawer.
- Closing the detail view returns the user to the same transaction list and filter state.

## Analytics

- Spending-by-category analytics are based on transaction amounts.
- Monthly spending is grouped using the transaction date.
- Analytics use the same underlying transaction dataset as the transaction table.
- Chart interactions are treated as filters on the transaction table where applicable.
- Clicking a category, payment method, or monthly trend data point applies the corresponding filter.

## Rewards

- Reward redemption consumes the required number of coins.
- A reward cannot be redeemed when the available balance is insufficient.
- Successful redemptions update the available balance.
- The reward catalogue is returned by the backend API.

## Backend

- PostgreSQL is the persistent database used by the application.
- FastAPI provides the REST API.
- SQLAlchemy is used for database access.
- Database validation and business rules are enforced on the backend rather than relying only on frontend validation.

## Frontend

- React is responsible for the dashboard interface and client-side interaction state.
- Vite is used for frontend development and production builds.
- The frontend communicates with the FastAPI backend through REST endpoints.
- Loading and error states are displayed when API requests are unavailable or fail.

## Scope

The assessment focuses on the requested transaction dashboard, analytics, filtering, transaction details, and rewards functionality.

Authentication, multi-user permissions, production payment processing, real-time transaction streaming, and external reward-provider integrations are outside the assessment scope unless explicitly required by the provided specification.