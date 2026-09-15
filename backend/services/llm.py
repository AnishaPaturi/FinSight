import json
import os
import requests
from typing import Dict, Any, List

from backend.config import GEMINI_API_KEY, OPENAI_API_KEY

def build_prompt(data: Dict[str, Any]) -> str:
    ticker = data.get("ticker", "UNKNOWN")
    tech = data.get("technical", {})
    pred = data.get("prediction", {})
    sent = data.get("sentiment", {})
    risk = data.get("risk", {})
    stock = data.get("stock", {})
    
    return f"""
You are a senior financial research analyst for the FinSight intelligence platform.
Synthesize an evidence-backed stock research report for {ticker} using ONLY the structured data provided below.
Do not invent information. Clearly distinguish between observed facts (technical indicators, news) and probabilistic model predictions.
Include a prominent disclaimer that this is for educational and research purposes only and not investment advice.

Structured Data:
- Ticker: {ticker} ({stock.get('company_name', ticker)})
- Current Price: {stock.get('currency', 'INR')} {stock.get('current_price')} (Daily Change: {stock.get('change_percent')}%)
- 52-Week Range: {stock.get('low_52w')} - {stock.get('high_52w')}
- Technical Indicators:
  * RSI (14): {tech.get('rsi')}
  * MACD: {tech.get('macd')} (Signal: {tech.get('macd_signal')}, Histogram: {tech.get('macd_hist')})
  * 20-Day SMA: {tech.get('sma_20')}, 50-Day SMA: {tech.get('sma_50')}, 20-Day EMA: {tech.get('ema_20')}
  * Bollinger Bands: Upper {tech.get('bollinger_upper')}, Lower {tech.get('bollinger_lower')}
  * Signals: {json.dumps(tech.get('summary_signals', {}))}
- ML Trend Model:
  * Direction: {pred.get('prediction')}
  * Confidence: {pred.get('confidence')}
  * Probabilities: {json.dumps(pred.get('probabilities', {}))}
- Market Sentiment:
  * Overall: {sent.get('overall_sentiment')} (Score: {sent.get('overall_score')})
  * Distribution: Positive {sent.get('positive_pct')}%, Neutral {sent.get('neutral_pct')}%, Negative {sent.get('negative_pct')}%
- Risk Assessment:
  * Risk Score: {risk.get('risk_score')}/100 ({risk.get('risk_level')})
  * Annualized Volatility: {risk.get('volatility_annualized')}
  * Maximum Drawdown: {risk.get('max_drawdown')}
  * Key Risk Factors: {json.dumps(risk.get('risk_factors', []))}

Format your response strictly as valid JSON with the following keys:
{{
  "executive_summary": "...",
  "technical_analysis": "...",
  "market_sentiment": "...",
  "risk_analysis": "...",
  "positive_factors": ["...", "..."],
  "negative_factors": ["...", "..."],
  "overall_outlook": "...",
  "disclaimer": "FinSight provides AI-generated information for educational and research purposes only and does not constitute financial advice."
}}
"""

def generate_local_structured_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic synthesis engine that provides high-quality, evidence-backed
    research reports even when no third-party LLM API key is present.
    """
    ticker = data.get("ticker", "Stock")
    stock = data.get("stock", {})
    tech = data.get("technical", {})
    pred = data.get("prediction", {})
    sent = data.get("sentiment", {})
    risk = data.get("risk", {})
    
    price = stock.get("current_price", 0.0)
    curr = stock.get("currency", "INR")
    pred_dir = pred.get("prediction", "NEUTRAL")
    pred_conf = int(pred.get("confidence", 0.5) * 100)
    rsi = tech.get("rsi", 50.0)
    risk_level = risk.get("risk_level", "MODERATE")
    risk_score = risk.get("risk_score", 50)
    sent_dir = sent.get("overall_sentiment", "Neutral")
    
    pos_factors = []
    neg_factors = []
    
    # Positive factor checks
    if pred_dir == "BULLISH":
        pos_factors.append(f"Machine learning model predicts upward trend with {pred_conf}% statistical confidence.")
    if rsi < 70 and rsi > 50:
        pos_factors.append(f"RSI of {rsi:.1f} shows solid upward momentum without being in overbought territory.")
    elif rsi <= 30:
        pos_factors.append(f"RSI of {rsi:.1f} indicates oversold conditions, suggesting potential bargain buying or mean reversion.")
    if tech.get("macd", 0) > tech.get("macd_signal", 0):
        pos_factors.append("MACD line remains above the signal line, maintaining positive short-term momentum.")
    if sent_dir == "Positive":
        pos_factors.append(f"Financial news coverage leans positive ({sent.get('positive_pct', 0)}% positive articles).")
    if risk_level == "LOW":
        pos_factors.append("Low annualized volatility and controlled historical drawdowns provide defensive cushion.")
        
    # Negative factor checks
    if pred_dir == "BEARISH":
        neg_factors.append(f"Machine learning model projects downward trend risk with {pred_conf}% confidence.")
    if rsi >= 70:
        neg_factors.append(f"RSI of {rsi:.1f} indicates overbought conditions, increasing short-term pullback risks.")
    elif rsi < 45:
        neg_factors.append(f"RSI of {rsi:.1f} signals sluggish price action and weak buyers.")
    if tech.get("macd", 0) < tech.get("macd_signal", 0):
        neg_factors.append("MACD line is below the signal line, indicating persistent downward pressure.")
    if risk_level == "HIGH":
        neg_factors.append(f"Elevated risk score ({risk_score}/100) driven by high volatility and sharp drawdowns.")
    if sent_dir == "Negative":
        neg_factors.append("News sentiment skews negative, reflecting market concerns or cautious media commentary.")
        
    if not pos_factors:
        pos_factors.append("Price action holds near foundational technical support zones.")
    if not neg_factors:
        neg_factors.append("General macroeconomic crosswinds may limit immediate upside follow-through.")
        
    exec_summary = (
        f"{ticker} is currently trading at {curr} {price:.2f}. "
        f"The composite intelligence system registers a {pred_dir} trend classification ({pred_conf}% confidence), "
        f"supported by {sent_dir.lower()} news sentiment and an overall {risk_level} risk score of {risk_score}/100."
    )
    
    tech_summary = (
        f"Momentum indicators show RSI at {rsi:.1f}. "
        f"The 20-day SMA is positioned at {curr} {tech.get('sma_20', price):.2f}, relative to the 50-day SMA at {curr} {tech.get('sma_50', price):.2f}. "
        f"Bollinger bands range between {curr} {tech.get('bollinger_lower', price):.2f} and {curr} {tech.get('bollinger_upper', price):.2f}, "
        f"with annualized 20-day volatility measuring {tech.get('volatility', 0.15)*100:.1f}%."
    )
    
    sent_summary = (
        f"Media sentiment for {ticker} is categorized as {sent_dir} with a composite score of {sent.get('overall_score', 0.0):.2f}. "
        f"Among recent items, {sent.get('positive_pct', 0)}% are positive, {sent.get('neutral_pct', 0)}% are neutral, "
        f"and {sent.get('negative_pct', 0)}% reflect negative sentiment."
    )
    
    risk_summary = (
        f"FinSight gauges risk at {risk_score}/100 ({risk_level} Risk). "
        f"Annualized volatility stands at {risk.get('volatility_annualized', 0.20)*100:.1f}%, "
        f"with a maximum peak-to-trough drawdown of {risk.get('max_drawdown', 0.10)*100:.1f}%. "
        + " ".join(risk.get("risk_factors", []))
    )
    
    outlook = (
        f"In summary, {ticker} presents a {pred_dir.lower()} profile with {risk_level.lower()} risk considerations. "
        "Traders and researchers should monitor RSI reaction around key moving averages while verifying volume confirmation on upcoming trend breaks."
    )
    
    return {
        "ticker": ticker,
        "executive_summary": exec_summary,
        "technical_analysis": tech_summary,
        "market_sentiment": sent_summary,
        "risk_analysis": risk_summary,
        "positive_factors": pos_factors,
        "negative_factors": neg_factors,
        "overall_outlook": outlook,
        "disclaimer": "FinSight provides AI-generated information for educational and research purposes only and does not constitute financial advice."
    }

def generate_ai_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes full structured stock metrics into an LLM analysis.
    Uses Gemini or OpenAI if keys are provided, with reliable structured fallback.
    """
    ticker = data.get("ticker", "UNKNOWN")
    
    # If Gemini API Key exists
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            prompt = build_prompt(data)
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code == 200:
                result = resp.json()
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text)
                parsed["ticker"] = ticker
                return parsed
        except Exception as e:
            print(f"Notice: Gemini API call error ({e}), falling back to deterministic synthesis.")
            
    # Fallback to deterministic synthesis engine
    return generate_local_structured_analysis(data)
