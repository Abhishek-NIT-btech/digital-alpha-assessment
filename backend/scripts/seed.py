from datetime import datetime, timezone
from decimal import Decimal

from dateutil import parser

import json
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.database import engine
from app.transaction import Transaction


def parse_timestamp(value):
    """
    Convert the different timestamp formats in the JSON
    into a timezone-aware datetime.
    """

    # Unix timestamp in milliseconds
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(
            value / 1000,
            tz=timezone.utc,
        )

    # String timestamp
    if isinstance(value, str):
        value = value.strip()

        parsed = parser.parse(value)

        # Treat timestamps without timezone information as UTC
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed

    raise ValueError(f"Unsupported timestamp value: {value}")


DATA_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "transactions_DA.json"
)


# -----------------------------
# Load JSON dataset
# -----------------------------

with open(DATA_FILE, "r", encoding="utf-8") as file:
    transactions = json.load(file)


print("Number of transactions:", len(transactions))


# -----------------------------
# Required field validation
# -----------------------------

EXPECTED_FIELDS = {
    "id",
    "timestamp",
    "merchant",
    "amount",
    "currency",
    "status",
    "payment_method",
}


invalid_transactions = []

for index, transaction in enumerate(transactions):
    missing_fields = EXPECTED_FIELDS - transaction.keys()

    if missing_fields:
        invalid_transactions.append(
            {
                "index": index,
                "id": transaction.get("id"),
                "missing_fields": sorted(missing_fields),
            }
        )


print("Invalid transactions:", len(invalid_transactions))


# -----------------------------
# Category validation
# -----------------------------

missing_categories = sum(
    1
    for transaction in transactions
    if not transaction.get("category")
    or not str(transaction.get("category")).strip()
)

print("Transactions without category:", missing_categories)


# -----------------------------
# Timestamp validation
# -----------------------------

timestamp_errors = []

for index, transaction in enumerate(transactions):
    try:
        parse_timestamp(transaction["timestamp"])

    except Exception as error:
        timestamp_errors.append(
            {
                "index": index,
                "id": transaction.get("id"),
                "timestamp": transaction.get("timestamp"),
                "error": str(error),
            }
        )


print("Timestamp errors:", len(timestamp_errors))


# -----------------------------
# Amount validation
# -----------------------------

amount_errors = []

for index, transaction in enumerate(transactions):
    amount = transaction.get("amount")

    try:
        Decimal(str(amount))

    except (TypeError, ValueError):
        amount_errors.append(
            {
                "index": index,
                "id": transaction.get("id"),
                "amount": amount,
            }
        )


print("Amount errors:", len(amount_errors))


if amount_errors:
    print("\nFirst 10 amount errors:")

    for item in amount_errors[:10]:
        print(item)
else:
    print("All amounts can be converted to numbers.")


# -----------------------------
# Unique values
# -----------------------------

categories = sorted(
    {
        transaction["category"]
        for transaction in transactions
        if transaction.get("category")
        and str(transaction.get("category")).strip()
    }
)

statuses = sorted(
    {
        transaction["status"]
        for transaction in transactions
    }
)

payment_methods = sorted(
    {
        transaction["payment_method"]
        for transaction in transactions
    }
)

currencies = sorted(
    {
        transaction["currency"]
        for transaction in transactions
    }
)


print("\nCategories:")
print(categories)

print("\nStatuses:")
print(statuses)

print("\nPayment methods:")
print(payment_methods)

print("\nCurrencies:")
print(currencies)


# -----------------------------
# Final validation
# -----------------------------

if (
    len(invalid_transactions) > 0
    or len(timestamp_errors) > 0
    or len(amount_errors) > 0
):
    print("\nData validation failed.")
    print("No data was inserted into PostgreSQL.")
    raise SystemExit(1)


print("\nData validation successful!")


# -----------------------------
# Prepare database models
# -----------------------------

transaction_models = []

for transaction in transactions:

    # Category can be missing or empty
    # in the source data.
    category = transaction.get("category")

    if not category or not str(category).strip():
        category = None

    # Convert numeric strings and numbers to Decimal.
    amount = Decimal(str(transaction["amount"]))

    # Normalize status values.
    # Example: "success" -> "SUCCESS"
    status = transaction["status"].upper()

    # Normalize timestamp.
    parsed_timestamp = parse_timestamp(
        transaction["timestamp"]
    )

    transaction_model = Transaction(
        # Original JSON ID.
        # The database generates its own primary key.
        transaction_id=transaction["id"],
        timestamp=parsed_timestamp,
        merchant=transaction["merchant"],
        category=category,
        amount=amount,
        currency=transaction["currency"],
        status=status,
        payment_method=transaction["payment_method"],
    )

    transaction_models.append(transaction_model)


print(
    f"Prepared {len(transaction_models)} transactions for insertion."
)


# -----------------------------
# Insert into PostgreSQL
# -----------------------------

with Session(engine) as session:

    try:
        # Clear existing transaction data.
        # This makes the seed script safe to run again.
        session.execute(delete(Transaction))

        # Insert all transactions.
        session.add_all(transaction_models)

        # Save changes.
        session.commit()

    except Exception:
        session.rollback()
        raise


print(
    f"Successfully seeded {len(transaction_models)} transactions."
)