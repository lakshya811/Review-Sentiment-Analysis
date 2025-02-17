"""
Module: logger.py
Description: Provides a MyLogger class that returns a configured logger with daily rotation.
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

class MyLogger:
    @staticmethod
    def get_logger(name: str = __name__):
        """
        Returns a logger instance configured for daily log rotation.
        Logs are stored in 'logs/app.log', rotated each midnight.
        Old log files are kept for 30 days by default.
        """
        # Ensure the logs/ directory exists.
        if not os.path.exists("logs"):
            os.mkdir("logs")

        # Create (or get) a logger.
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Avoid adding multiple handlers if get_logger is called multiple times.
        if not logger.handlers:
            # Create a TimedRotatingFileHandler that rotates daily at midnight.
            log_file = os.path.join("logs", "app.log")
            handler = TimedRotatingFileHandler(
                filename=log_file,
                when="midnight",       # Rotate at midnight
                interval=1,           # Every 1 day
                backupCount=30,       # Keep 30 old log files
                encoding="utf-8",
                utc=False             # Rotate based on local time
            )
            # By default, TimedRotatingFileHandler uses append mode.

            # Create a formatter and set it for the handler.
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)

            # Add the handler to the logger.
            logger.addHandler(handler)

        return logger
