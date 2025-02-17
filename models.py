"""
Module: models.py
Description: Contains Pydantic models for product review requests and responses.
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
# ---------------------
# Request Models
# ---------------------

class ProductReviewData(BaseModel):
    """
    Holds the actual product review text.
    """
    review_text: str = Field(..., description="The text of the product review.")


class ProductReviewRequest(BaseModel):
    """
    Request body for submitting a product review for sentiment analysis.
    """
    request_id: str = Field(..., description="Unique request identifier (UUID as string).")
    user_id: str = Field(..., description="Unique identifier of the user.")
    data: ProductReviewData = Field(..., description="Data containing the actual review text.")

# ---------------------
# Response Models
# ---------------------

class ProductReviewResponseData(BaseModel):
    """
    Contains the data part of the response, holding status, sentiment, etc.
    """
    request_id: str
    user_id: str
    status: str                          # e.g., "COMPLETED" or "ERROR"
    error_message: Optional[str] = None  # Holds an error message if status is "ERROR"
    sentiment: Optional[str] = None      # e.g., "positive", "negative", "neutral"
    confidence: Optional[int] = None     # e.g., 80 (if 80% confident), or None if error


class ProductReviewResponse(BaseModel):
    """
    Overall response model for both success (200) and error (400/500).
    """
    status_code: int
    success: bool
    message: str
    data: ProductReviewResponseData

# ---------------------
# Metrics Model
# ---------------------

class MetricsData(BaseModel):
    """
    Represents a single record of metrics data to be written to CSV.
    """
    request_id: str
    user_id: str
    review_text: str
    sentiment: str  # e.g., "positive", "negative", "neutral"
    average_confidence_score: int
    execution_time: float  # in seconds
    datetime: str = Field(
        default_factory=lambda: datetime.now().isoformat()
    )

# ---------------------
# Data Retreival
# ---------------------
class Dataretrieve(BaseModel):
    id : str