import unittest

from sqlalchemy import text

try:
    from app.database import engine
except ModuleNotFoundError:
    from database import engine


class DatabaseTest(unittest.TestCase):
    def test_database_connection(self):
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()

        self.assertEqual(value, 1)


if __name__ == "__main__":
    unittest.main()