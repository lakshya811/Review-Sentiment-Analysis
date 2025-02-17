"""
Module: mydb.py
Description: Handles SQLite database connection, creation, and data insertion.
"""

import sqlite3
from logger import MyLogger
from databases import Database
# Get a logger for this module
logger = MyLogger.get_logger(__name__)

# Specify the name (or path) of the SQLite database file.
DB_FILE = "sentiment_analysis.db"
file = Database("sqlite:///sentiment_analysis.db")
def create_database():
    """
    Creates the SQLite database and reviews table if they do not exist.
    Includes exception handling for any issues during creation.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # Create a table for storing reviews and their sentiment analysis results.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    review_text TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()

        logger.info("Database and reviews table checked/created successfully.")

    except Exception as e:
        logger.error(f"Error creating database or table: {e}")
        raise
def retrive_data_user(
        u_id:str
):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor= conn.cursor()
            cursor.execute("""
                SELECT * FROM reviews where user_id = {}
                           """)
            output = cursor.fetchmany() 
            for row in output: 
                print(row) 
            conn.commit()
    except Exception as e:
        logger.error(f"Error inserting feedback: {e}")
        raise

def retrive_data():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor= conn.cursor()
            cursor.execute("""
                SELECT * FROM reviews
                           """)
            output = cursor.fetchmany() 
            for row in output: 
                print(row)
            conn.commit()
    except Exception as e:
        logger.error(f"Error inserting feedback: {e}")
        raise


def insert_feedback(
    request_id: str,
    user_id: str,
    review_text: str,
    sentiment: str,
    confidence: float
):
    """
    Inserts feedback data into the reviews table.

    Args:
        request_id (str): Unique ID for the request (e.g., UUID).
        user_id (str): Unique ID for the user.
        review_text (str): The text of the product review.
        sentiment (str): The computed sentiment label (positive, negative, neutral).
        confidence (float): The sentiment confidence score (0.0 to 1.0).
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reviews (request_id, user_id, review_text, sentiment, confidence)
                VALUES (?, ?, ?, ?, ?)
            """, (request_id, user_id, review_text, sentiment, confidence))
            conn.commit()

        logger.info(
            f"insert_feedback - Inserted feedback for request_id={request_id}, "
            f"user_id={user_id}, sentiment={sentiment}, confidence={confidence}"
        )

    except Exception as e:
        logger.error(f"Error inserting feedback: {e}")
        raise
