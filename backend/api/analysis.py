from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any

from backend.models.stock_model import (
    TechnicalIndicatorsResponse,
    PredictionResponse,
    SentimentResponse,
    RiskResponse,
    AIAnalysisResponse,
    FullAnalysisResponse,
    PricePoint,
    StockOverview
)
from backend.services.market_data import get_stock_data
from backend.services.technical_analysis import calculate_indicators, extract_latest_indicators
from backend.services.prediction import predict_trend
from backend.services.sentiment import get_stock_sentiment
from backend.services.risk import calculate_risk
from backend.services.llm import generate_ai_analysis

router = APIRouter(prefix="/api", tags=["Analysis & Intelligence"])

class ChatRequest(BaseModel):
    ticker: str
    question: str

class ChatResponse(BaseModel):
    ticker: str
    question: str
    answer: str
    route_used: str

@router.get("/technical/{ticker}", response_model=TechnicalIndicatorsResponse)
def get_technical_analysis(ticker: str):
    df, overview = get_stock_data(ticker, period="1y")
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock data unavailable")
    df_calc = calculate_indicators(df)
    indicators = extract_latest_indicators(df_calc, overview["ticker"])
    return TechnicalIndicatorsResponse(**indicators)

@router.get("/prediction/{ticker}", response_model=PredictionResponse)
def get_ml_prediction(ticker: str):
    df, overview = get_stock_data(ticker, period="1y")
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock data unavailable")
    pred = predict_trend(df, overview["ticker"])
    return PredictionResponse(**pred)

@router.get("/sentiment/{ticker}", response_model=SentimentResponse)
def get_sentiment(ticker: str):
    data = get_stock_sentiment(ticker)
    return SentimentResponse(**data)

@router.get("/risk/{ticker}", response_model=RiskResponse)
def get_risk_analysis(ticker: str):
    df, overview = get_stock_data(ticker, period="1y")
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock data unavailable")
    risk = calculate_risk(df, overview["ticker"])
    return RiskResponse(**risk)

@router.get("/analysis/{ticker}", response_model=AIAnalysisResponse)
def get_ai_report(ticker: str):
    df, overview = get_stock_data(ticker, period="1y")
    if df.empty:
        raise HTTPException(status_code=404, detail="Stock data unavailable")
    df_calc = calculate_indicators(df)
    tech = extract_latest_indicators(df_calc, overview["ticker"])
    pred = predict_trend(df, overview["ticker"])
    sent = get_stock_sentiment(overview["ticker"])
    risk = calculate_risk(df, overview["ticker"])
    
    analysis_input = {
        "ticker": overview["ticker"],
        "stock": overview,
        "technical": tech,
        "prediction": pred,
        "sentiment": sent,
        "risk": risk
    }
    ai_report = generate_ai_analysis(analysis_input)
    return AIAnalysisResponse(**ai_report)

@router.get("/full-analysis/{ticker}", response_model=FullAnalysisResponse)
def get_full_analysis(ticker: str):
    """
    Primary FinSight endpoint: aggregates historical market data,
    technical indicators, ML trend prediction, sentiment, risk engine,
    and LLM analysis into a unified response for dashboard rendering.
    """
    df, overview = get_stock_data(ticker, period="1y")
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Stock data not found for ticker: {ticker}")
        
    df_calc = calculate_indicators(df)
    tech = extract_latest_indicators(df_calc, overview["ticker"])
    pred = predict_trend(df, overview["ticker"])
    sent = get_stock_sentiment(overview["ticker"])
    risk = calculate_risk(df, overview["ticker"])
    
    analysis_input = {
        "ticker": overview["ticker"],
        "stock": overview,
        "technical": tech,
        "prediction": pred,
        "sentiment": sent,
        "risk": risk
    }
    ai_report = generate_ai_analysis(analysis_input)
    
    # Format historical price list (last 180 points for fast chart loading)
    chart_df = df_calc.tail(180)
    prices = [
        PricePoint(
            date=row["Date"],
            open=round(float(row["Open"]), 2),
            high=round(float(row["High"]), 2),
            low=round(float(row["Low"]), 2),
            close=round(float(row["Close"]), 2),
            volume=int(row["Volume"])
        )
        for _, row in chart_df.iterrows()
    ]
    
    return FullAnalysisResponse(
        stock=StockOverview(**overview),
        historical=prices,
        technical=TechnicalIndicatorsResponse(**tech),
        prediction=PredictionResponse(**pred),
        sentiment=SentimentResponse(**sent),
        risk=RiskResponse(**risk),
        ai_analysis=AIAnalysisResponse(**ai_report)
    )

@router.post("/chat", response_model=ChatResponse)
def chat_with_finsight(req: ChatRequest):
    """
    Model Router: Classifies user query to appropriate analytical subsystem
    (Numerical analytics, ML prediction, News sentiment, Risk, or Synthesis LLM).
    """
    q_lower = req.question.lower()
    ticker = req.ticker.upper()
    
    df, overview = get_stock_data(ticker, period="1y")
    if df.empty:
        return ChatResponse(
            ticker=ticker,
            question=req.question,
            answer=f"Could not locate data for ticker {ticker}.",
            route_used="Error"
        )
        
    df_calc = calculate_indicators(df)
    tech = extract_latest_indicators(df_calc, ticker)
    pred = predict_trend(df, ticker)
    sent = get_stock_sentiment(ticker)
    risk = calculate_risk(df, ticker)
    
    curr = overview.get("currency", "INR")
    price = overview.get("current_price")
    
    # 1. Numerical / Indicator queries
    if any(k in q_lower for k in ["rsi", "sma", "ema", "macd", "bollinger", "price", "value"]):
        route = "Numerical Analytics Engine"
        if "rsi" in q_lower:
            answer = f"The 14-day RSI for {ticker} is currently {tech.get('rsi')} ({tech.get('summary_signals', {}).get('RSI', 'Neutral')})."
        elif "price" in q_lower:
            answer = f"{ticker} is currently trading at {curr} {price:.2f} ({overview.get('change_percent'):+.2f}% today)."
        elif "macd" in q_lower:
            answer = f"The MACD for {ticker} is {tech.get('macd')} (Signal: {tech.get('macd_signal')}, Histogram: {tech.get('macd_hist')}). Signal: {tech.get('summary_signals', {}).get('MACD')}."
        else:
            answer = f"Technical summary for {ticker}: 20-day SMA is {curr} {tech.get('sma_20')}, 50-day SMA is {curr} {tech.get('sma_50')}, Volatility is {tech.get('volatility')*100:.1f}%."
            
    # 2. Prediction / Trend queries
    elif any(k in q_lower for k in ["predict", "prediction", "trend", "bullish", "bearish", "direction"]):
        route = "ML Trend Classifier"
        answer = f"FinSight's machine learning model classifies {ticker}'s short-term trend as {pred.get('prediction')} with {int(pred.get('confidence', 0)*100)}% confidence."
        
    # 3. Sentiment / News queries
    elif any(k in q_lower for k in ["news", "sentiment", "media", "articles", "headline"]):
        route = "NLP Sentiment Engine"
        answer = f"Market sentiment for {ticker} is currently {sent.get('overall_sentiment')} (score: {sent.get('overall_score'):+.2f}). Breakdown: {sent.get('positive_pct')}% positive, {sent.get('neutral_pct')}% neutral, {sent.get('negative_pct')}% negative."
        
    # 4. Risk queries
    elif any(k in q_lower for k in ["risk", "safe", "drawdown", "danger", "volatile", "volatility"]):
        route = "Risk Assessment Engine"
        factors = "; ".join(risk.get("risk_factors", []))
        answer = f"{ticker} has a risk score of {risk.get('risk_score')}/100, categorized as {risk.get('risk_level')} risk. Annualized volatility is {risk.get('volatility_annualized')*100:.1f}% and maximum drawdown is {risk.get('max_drawdown')*100:.1f}%. Observed factors: {factors}."
        
    # 5. General synthesis / explanation
    else:
        route = "LLM Synthesis Router"
        ai_rep = generate_ai_analysis({
            "ticker": ticker,
            "stock": overview,
            "technical": tech,
            "prediction": pred,
            "sentiment": sent,
            "risk": risk
        })
        answer = ai_rep.get("executive_summary") + " " + ai_rep.get("overall_outlook")
        
    return ChatResponse(
        ticker=ticker,
        question=req.question,
        answer=answer,
        route_used=route
    )
