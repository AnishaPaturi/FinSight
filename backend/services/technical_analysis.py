import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    """Calculates Simple Moving Average."""
    return series.rolling(window=window, min_periods=1).mean()

def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    """Calculates Exponential Moving Average."""
    return series.ewm(span=span, adjust=False).mean()

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculates Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    # Exponential rolling average for smooth RSI
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    # Fill leading NaNs
    return rsi.fillna(50.0)

def calculate_macd(
    series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculates MACD Line, Signal Line, and MACD Histogram."""
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    macd_hist = macd_line - signal_line
    return macd_line, signal_line, macd_hist

def calculate_bollinger_bands(
    series: pd.Series, window: int = 20, num_std: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculates Bollinger Bands (Upper, Middle, Lower)."""
    middle = series.rolling(window=window, min_periods=1).mean()
    std = series.rolling(window=window, min_periods=1).std().fillna(0)
    upper = middle + (std * num_std)
    lower = middle - (std * num_std)
    return upper, middle, lower

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes all core technical indicators and adds them as columns to df.
    Columns added:
    - Return, Volatility_20
    - SMA_20, SMA_50
    - EMA_20
    - RSI_14
    - MACD, MACD_Signal, MACD_Hist
    - BB_Upper, BB_Middle, BB_Lower
    """
    data = df.copy()
    close = data["Close"]
    
    # Returns and volatility
    data["Return"] = close.pct_change().fillna(0.0)
    data["Volatility_20"] = data["Return"].rolling(window=20, min_periods=5).std().fillna(0.0) * np.sqrt(252)
    
    # Trend
    data["SMA_20"] = calculate_sma(close, 20)
    data["SMA_50"] = calculate_sma(close, 50)
    data["EMA_20"] = calculate_ema(close, 20)
    
    # Momentum & Oscillators
    data["RSI_14"] = calculate_rsi(close, 14)
    macd_line, macd_signal, macd_hist = calculate_macd(close, 12, 26, 9)
    data["MACD"] = macd_line
    data["MACD_Signal"] = macd_signal
    data["MACD_Hist"] = macd_hist
    
    # Bands
    bb_u, bb_m, bb_l = calculate_bollinger_bands(close, 20, 2.0)
    data["BB_Upper"] = bb_u
    data["BB_Middle"] = bb_m
    data["BB_Lower"] = bb_l
    
    # Momentum (10-day price return)
    data["Momentum_10"] = close.pct_change(periods=10).fillna(0.0)
    
    return data

def extract_latest_indicators(df_with_indicators: pd.DataFrame, ticker: str) -> Dict[str, Any]:
    """
    Extracts the latest indicator values and interprets signal directions.
    """
    if df_with_indicators.empty:
        return {}
        
    latest = df_with_indicators.iloc[-1]
    prev = df_with_indicators.iloc[-2] if len(df_with_indicators) > 1 else latest
    
    price = float(latest["Close"])
    rsi = float(latest.get("RSI_14", 50.0))
    macd = float(latest.get("MACD", 0.0))
    macd_signal = float(latest.get("MACD_Signal", 0.0))
    macd_hist = float(latest.get("MACD_Hist", 0.0))
    sma_20 = float(latest.get("SMA_20", price))
    sma_50 = float(latest.get("SMA_50", price))
    ema_20 = float(latest.get("EMA_20", price))
    bb_upper = float(latest.get("BB_Upper", price * 1.05))
    bb_middle = float(latest.get("BB_Middle", price))
    bb_lower = float(latest.get("BB_Lower", price * 0.95))
    volatility = float(latest.get("Volatility_20", 0.15))
    daily_return = float(latest.get("Return", 0.0))
    
    signals = {}
    
    # RSI Signal
    if rsi >= 70:
        signals["RSI"] = "Overbought (Bearish potential)"
    elif rsi <= 30:
        signals["RSI"] = "Oversold (Bullish potential)"
    elif rsi > 55:
        signals["RSI"] = "Bullish momentum"
    elif rsi < 45:
        signals["RSI"] = "Bearish momentum"
    else:
        signals["RSI"] = "Neutral"
        
    # MACD Signal
    if macd > macd_signal and macd_hist > 0:
        signals["MACD"] = "Bullish crossover"
    elif macd < macd_signal and macd_hist < 0:
        signals["MACD"] = "Bearish crossover"
    else:
        signals["MACD"] = "Neutral / Divergence"
        
    # Moving Average Signal
    if price > sma_20 and sma_20 > sma_50:
        signals["MovingAverages"] = "Strong Uptrend (Price > SMA20 > SMA50)"
    elif price < sma_20 and sma_20 < sma_50:
        signals["MovingAverages"] = "Downtrend (Price < SMA20 < SMA50)"
    elif price > sma_20:
        signals["MovingAverages"] = "Mild Bullish (Above SMA20)"
    else:
        signals["MovingAverages"] = "Mild Bearish (Below SMA20)"
        
    # Bollinger Bands Signal
    if price >= bb_upper:
        signals["BollingerBands"] = "Price touching upper band (Upper resistance)"
    elif price <= bb_lower:
        signals["BollingerBands"] = "Price near lower band (Potential support)"
    else:
        signals["BollingerBands"] = "Within normal distribution"
        
    return {
        "ticker": ticker,
        "current_price": round(price, 2),
        "sma_20": round(sma_20, 2),
        "sma_50": round(sma_50, 2),
        "ema_20": round(ema_20, 2),
        "rsi": round(rsi, 2),
        "macd": round(macd, 2),
        "macd_signal": round(macd_signal, 2),
        "macd_hist": round(macd_hist, 2),
        "bollinger_upper": round(bb_upper, 2),
        "bollinger_middle": round(bb_middle, 2),
        "bollinger_lower": round(bb_lower, 2),
        "volatility": round(volatility, 4),
        "daily_return": round(daily_return, 4),
        "summary_signals": signals
    }
