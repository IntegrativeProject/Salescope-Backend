import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT", "5432"),
        }

        # Validate missing variables
        missing = [k for k, v in self.db_config.items() if not v]
        if missing:
            raise EnvironmentError(f"Missing environment variables: {missing}")

        self.conn = None
        self.cursor = None
    
    def get_url(self):
        return self.database_url

    # ------------------------------
    # Context Manager Methods
    # ------------------------------
    def __enter__(self):
        """Handles the connection automatically when using 'with'."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            print("Database connected successfully.")
        except Error as e:
            print(f"Connection error: {e}")
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the connection when leaving 'with' block."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")

    # ------------------------------
    # Regular methods
    # ------------------------------
    def execute(self, query, params=None, fetch=False):
        """Executes SQL queries safely."""
        try:
            self.cursor.execute(query, params)

            if fetch:
                return self.cursor.fetchall()

            self.conn.commit()

        except Error as e:
            print(f"Query error: {e}")
            self.conn.rollback()
            raise


# ======================================================
# Example of usage
# ======================================================
if __name__ == "__main__":
    with DatabaseConnection() as db:
        version = db.execute("SELECT version();", fetch=True)
        print(f"📌 PostgreSQL version: {version}")
