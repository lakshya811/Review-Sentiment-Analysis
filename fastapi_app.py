"""
FastAPI application that secures a review-sentiment endpoint with a static Bearer token.
The token is read from the SECRET_KEY environment variable.
"""

import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import (
    ProductReviewRequest,
    ProductReviewResponse,
    ProductReviewResponseData,
    MetricsData,
    Dataretrieve
)
from sentiment_analysis import analyze_sentiment
from logger import MyLogger
import my_db 
from my_db import file
from metrics_writer import write_metrics_record

# Load environment variables from a .env file if present.
load_dotenv()

# Configure logger for this module
logger = MyLogger.get_logger(__name__)

# Retrieve the static token from SECRET_KEY, or use a default.
SECRET_KEY = os.getenv("SECRET_KEY", "MY_VERY_SECRET_TOKEN")

# HTTPBearer is a FastAPI security utility that extracts "Authorization: Bearer <token>"
auth_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Verifies the Bearer token against SECRET_KEY.
    Raises 401 if the token doesn't match.
    """
    token = credentials.credentials
    if token != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token

# Initialize the FastAPI application instance.
app = FastAPI(
    title="Product Review Sentiment Analysis",
    description="Analyzes sentiment of product reviews, secured by a static Bearer token.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """
    Called when the FastAPI application starts.
    Ensures the database and necessary tables are created.
    """
    logger.info("Application startup: Initializing database.")
    my_db.create_database()  # Create/Verify the database and table existence.

@app.post("/data_all_db")
async def retrieve_data_db(token: str = Depends(verify_token)):

    try:
        query = "SELECT * FROM reviews"
        results = await file.fetch_all(query=query)

        return  results
    except Exception as e:
        print(e)

@app.post("/data_db",tags=["Data Retrieval"])
async def fetch_data(id: Dataretrieve,token: str = Depends(verify_token)):
    try:
        query = "SELECT * FROM reviews WHERE user_id={}".format(str(id.id))
        results = await file.fetch_all(query=query)

        return  results
    except Exception as e:
        print(e)

@app.post("/reviews", response_model=ProductReviewResponse, tags=["Sentiment Analysis"])
async def analyze_product_review(
    review_request: ProductReviewRequest,
    token: str = Depends(verify_token)
) -> ProductReviewResponse:
    """
    POST endpoint for analyzing a product review.
    The caller must provide a valid Bearer token matching SECRET_KEY.
    Returns a structured response with sentiment data or error details.
    """
    start_time = time.perf_counter()
    try:
        logger.info(
            f"analyze_product_review - Received request_id={review_request.request_id}, "
            f"user_id={review_request.user_id}"
        )

        # Perform sentiment analysis on the provided review text.
        result = analyze_sentiment(review_request.data.review_text)

        # Convert float confidence (e.g., 0.85) to integer (85).
        confidence_int = int(result["confidence"] * 100)

        # Store the feedback data into the database.
        my_db.insert_feedback(
            request_id=review_request.request_id,
            user_id=review_request.user_id,
            review_text=review_request.data.review_text,
            sentiment=result["sentiment"],
            confidence=result["confidence"]  # stored as float 0-1
        )
        
        # Build a success response with status_code=200 and success=True.
        response_data = ProductReviewResponseData(
            request_id=review_request.request_id,
            user_id=review_request.user_id,
            status="COMPLETED",
            error_message=None,
            sentiment=result["sentiment"],
            confidence=confidence_int
        )

        # Calculate execution time
        end_time = time.perf_counter()
        execution_time = end_time - start_time
       
        # Write metrics to CSV
        write_metrics_record(
            MetricsData(
                request_id=review_request.request_id,
                user_id=review_request.user_id,
                review_text=review_request.data.review_text,
                sentiment=result["sentiment"],
                average_confidence_score=confidence_int,
                execution_time=execution_time
            )
        )

        logger.info(
            f"analyze_product_review - Successfully processed request_id={review_request.request_id}"
        )

        return ProductReviewResponse(
            status_code=200,
            success=True,
            message="completed",
            data=response_data
        )

    except Exception as exc:
        # On any exception, return a structured error with status_code=500 and success=False.
        logger.error(f"analyze_product_review - Error for request_id={review_request.request_id}: {exc}")
        response_data = ProductReviewResponseData(
            request_id=review_request.request_id,
            user_id=review_request.user_id,
            status="ERROR",
            error_message=str(exc),
            sentiment=None,
            confidence=None
        )
        return ProductReviewResponse(
            status_code=500,
            success=False,
            message="An error occurred while calculating sentiment",
            data=response_data
        )
# Entry point for local development: run with `python main.py`.
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on host=0.0.0.0, port=8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
