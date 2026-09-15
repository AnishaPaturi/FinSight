from fastapi import APIRouter, HTTPException, Query
from typing import List

from backend.models.stock_model import StockOverview, HistoricalDataResponse, PricePoint
from backend.services.market_data import get_stock_data

router = APIRouter(prefix="/api/stock", tags=["Stock Data"])

@router.get("/{ticker}", response_model=StockOverview)
def get_stock_overview(ticker: str):
    """Fetches real-time / current market summary for a stock."""
    df, overview = get_stock_data(ticker, period="1y")
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Stock data not found for ticker: {ticker}")
    return StockOverview(**overview)

@router.get("/{ticker}/history", response_model=HistoricalDataResponse)
def get_stock_history(
    ticker: str,
    period: str = Query("1y", description="Data period (1mo, 3mo, 6mo, 1y, 2y, 5y)"),
    interval: str = Query("1d", description="Candle interval (1d, 1wk)")
):
    """Fetches historical OHLCV candles for charting."""
    df, overview = get_stock_data(ticker, period=period, interval=interval)
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Stock history not found for ticker: {ticker}")
        
    prices = [
        PricePoint(
            date=row["Date"],
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=int(row["Volume"])
        )
        for _, row in df.iterrows()
    ]
    
    return HistoricalDataResponse(
        ticker=overview["ticker"],
        company_name=overview["company_name"],
        count=len(prices),
        prices=prices
    )
