from fastapi import APIRouter
from backend.models.stock_model import SentimentResponse
from backend.services.sentiment import get_stock_sentiment

router = APIRouter(prefix="/api/news", tags=["News & Sentiment"])

@router.get("/{ticker}", response_model=SentimentResponse)
def get_news_and_sentiment(ticker: str):
    """Fetches news and sentiment classification for the specified ticker."""
    sentiment_data = get_stock_sentiment(ticker)
    return SentimentResponse(**sentiment_data)
