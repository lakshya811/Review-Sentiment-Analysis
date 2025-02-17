"""
Module: metrics_writer.py
Description: Writes sentiment analysis metrics to a CSV file in the 'metrics/' directory.
"""

import csv
import os
from logger import MyLogger
from models import MetricsData

logger = MyLogger.get_logger(__name__)

METRICS_DIR = "metrics"
METRICS_FILE = os.path.join(METRICS_DIR, "Metrics.csv")

def write_metrics_record(record: MetricsData):
    """
    Writes a single metrics record to 'Metrics.csv' in 'metrics/' directory.
    Creates the directory and file if not present, and appends new entries otherwise.
    """
    # Create 'metrics/' if it doesn't exist
    if not os.path.exists(METRICS_DIR):
        os.mkdir(METRICS_DIR)
        logger.info(f"Created directory: {METRICS_DIR}")

    # Check if the CSV file already exists (to know if we need a header)
    file_exists = os.path.isfile(METRICS_FILE)

    try:
        with open(METRICS_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header if file did not exist before
            if not file_exists:
                writer.writerow([
                    "datetime",
                    "request_id",
                    "user_id",
                    "review_text",
                    "sentiment",
                    "average_confidence_score",
                    "execution_time"
                ])

            # Write the actual metrics row
            writer.writerow([
                record.datetime,
                record.request_id,
                record.user_id,
                record.review_text,
                record.sentiment,
                record.average_confidence_score,
                record.execution_time
            ])

        logger.info(f"Metrics record written for request_id={record.request_id} to {METRICS_FILE}")

    except Exception as e:
        logger.error(f"Error writing metrics record for request_id={record.request_id}: {e}")
        raise
