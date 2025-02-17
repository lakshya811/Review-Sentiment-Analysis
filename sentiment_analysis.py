"""
Module: sentiment_analysis.py
Description: Provides functions to analyze text sentiment using TextBlob
"""

from textblob import TextBlob
from logger import MyLogger

# Get a logger for this module
logger = MyLogger.get_logger(__name__)


def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of the given text using TextBlob for sentiment scoring.

    Args:
        text (str): The input text for sentiment analysis.

    Returns:
        dict: A dictionary containing:
              - 'sentiment': The sentiment label (positive, negative, neutral).
              - 'confidence': The confidence score (scaled by polarity).

    Example:
        >>> analyze_sentiment("I love this product!")
        {
            "sentiment": "positive",
            "confidence": 0.5
        }
    """

    # Use TextBlob for a simple sentiment polarity score.
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Range: -1.0 (most negative) to 1.0 (most positive)

    # Classify sentiment based on polarity.
    if polarity > 0:
        sentiment_label = "positive"
    elif polarity < 0:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"

    # Use the absolute polarity value as a naive confidence measure.
    confidence_score = abs(polarity)

    logger.info(
        f"analyze_sentiment - Text length: {len(text)}, "
        f"Polarity: {polarity}, Sentiment: {sentiment_label}, Confidence: {confidence_score}"
    )

    return {
        "sentiment": sentiment_label,
        "confidence": round(confidence_score, 2)  # Round to 2 decimals for readability
    }

