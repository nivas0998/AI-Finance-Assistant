import sqlite3

DATABASE_NAME = "finance.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,
            category TEXT,
            limit_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    connection.commit()
    connection.close()