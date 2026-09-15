import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.market_data import get_stock_data
from backend.services.technical_analysis import calculate_indicators, extract_latest_indicators
from backend.services.prediction import predict_trend
from backend.services.risk import calculate_risk
from backend.services.sentiment import get_stock_sentiment

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "endpoints" in data

def test_market_data_and_indicators():
    df, overview = get_stock_data("RELIANCE", period="6mo")
    assert not df.empty
    assert "Close" in df.columns
    assert overview["ticker"] == "RELIANCE"
    
    df_calc = calculate_indicators(df)
    assert "SMA_20" in df_calc.columns
    assert "RSI_14" in df_calc.columns
    assert "MACD" in df_calc.columns
    assert "BB_Upper" in df_calc.columns
    
    latest = extract_latest_indicators(df_calc, "RELIANCE")
    assert "rsi" in latest
    assert "macd" in latest
    assert "summary_signals" in latest

def test_prediction_service():
    df, _ = get_stock_data("TCS", period="6mo")
    pred = predict_trend(df, "TCS")
    assert pred["ticker"] == "TCS"
    assert pred["prediction"] in ["BULLISH", "BEARISH", "NEUTRAL"]
    assert 0.0 <= pred["confidence"] <= 1.0

def test_risk_service():
    df, _ = get_stock_data("INFY", period="6mo")
    risk = calculate_risk(df, "INFY")
    assert risk["ticker"] == "INFY"
    assert 0 <= risk["risk_score"] <= 100
    assert risk["risk_level"] in ["LOW", "MODERATE", "HIGH"]
    assert isinstance(risk["risk_factors"], list)

def test_sentiment_service():
    sent = get_stock_sentiment("AAPL")
    assert sent["ticker"] == "AAPL"
    assert sent["overall_sentiment"] in ["Positive", "Neutral", "Negative"]
    assert -1.0 <= sent["overall_score"] <= 1.0
    assert len(sent["articles"]) > 0

def test_full_analysis_api():
    response = client.get("/api/full-analysis/RELIANCE")
    assert response.status_code == 200
    data = response.json()
    assert "stock" in data
    assert "technical" in data
    assert "prediction" in data
    assert "sentiment" in data
    assert "risk" in data
    assert "ai_analysis" in data
    assert len(data["historical"]) > 0

def test_chat_router():
    # Test numerical query
    resp1 = client.post("/api/chat", json={"ticker": "RELIANCE", "question": "What is the RSI?"})
    assert resp1.status_code == 200
    assert "RSI" in resp1.json()["answer"]
    
    # Test risk query
    resp2 = client.post("/api/chat", json={"ticker": "RELIANCE", "question": "Why is this stock risky?"})
    assert resp2.status_code == 200
    assert "risk" in resp2.json()["answer"].lower()
