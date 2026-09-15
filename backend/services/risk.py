import pandas as pd
import numpy as np
from typing import Dict, Any, List

def calculate_max_drawdown(series: pd.Series) -> float:
    """Calculates peak-to-trough maximum drawdown."""
    if series.empty:
        return 0.0
    cummax = series.cummax()
    drawdown = (series - cummax) / cummax.replace(0, np.nan)
    max_dd = float(abs(drawdown.min()))
    return round(max_dd, 4) if not np.isnan(max_dd) else 0.0

def calculate_risk(df: pd.DataFrame, ticker: str) -> Dict[str, Any]:
    """
    Computes a comprehensive risk score (0-100), risk level (LOW/MODERATE/HIGH),
    and identified risk/mitigation factors based on volatility, drawdown, and volume.
    """
    if df.empty or len(df) < 10:
        return {
            "ticker": ticker,
            "risk_score": 50,
            "risk_level": "MODERATE",
            "volatility_annualized": 0.20,
            "max_drawdown": 0.10,
            "volume_anomaly": False,
            "rsi_extreme": False,
            "risk_factors": ["Insufficient historical data to determine granular risk profile."]
        }
        
    close = df["Close"]
    volume = df["Volume"]
    
    # 1. Volatility
    returns = close.pct_change().dropna()
    volatility = float(returns.tail(30).std() * np.sqrt(252)) if len(returns) >= 5 else 0.20
    if np.isnan(volatility):
        volatility = 0.20
        
    # 2. Maximum Drawdown (past 1 year or entire window)
    lookback = min(len(close), 252)
    max_dd = calculate_max_drawdown(close.tail(lookback))
    
    # 3. Volume Anomaly
    avg_vol = float(volume.tail(20).mean()) if len(volume) >= 5 else float(volume.iloc[-1])
    latest_vol = float(volume.iloc[-1])
    vol_ratio = latest_vol / avg_vol if avg_vol > 0 else 1.0
    volume_anomaly = bool(vol_ratio >= 2.0)
    
    # 4. RSI Extremes
    delta = close.diff()
    gain = delta.clip(lower=0).tail(14).mean()
    loss = -delta.clip(upper=0).tail(14).mean()
    rs = gain / (loss if loss > 0 else 1e-6)
    current_rsi = 100 - (100 / (1 + rs)) if not np.isnan(rs) else 50.0
    rsi_extreme = bool(current_rsi >= 75 or current_rsi <= 25)
    
    # 5. Recent daily shock
    latest_return = abs(float(returns.iloc[-1])) if len(returns) > 0 else 0.0
    daily_shock = bool(latest_return >= 0.035)
    
    # Score calculation
    score = 50
    factors: List[str] = []
    
    # Volatility impact
    if volatility >= 0.35:
        score += 16
        factors.append(f"Elevated annualized volatility ({volatility*100:.1f}%) signals high price fluctuations.")
    elif volatility >= 0.25:
        score += 8
        factors.append(f"Moderate annualized volatility ({volatility*100:.1f}%).")
    elif volatility <= 0.16:
        score -= 10
        factors.append(f"Stable price volatility ({volatility*100:.1f}%) lowers downside turbulence.")
        
    # Drawdown impact
    if max_dd >= 0.25:
        score += 15
        factors.append(f"Significant peak-to-trough drawdown of {max_dd*100:.1f}% observed.")
    elif max_dd >= 0.15:
        score += 8
        factors.append(f"Noticeable recent pullback with {max_dd*100:.1f}% max drawdown.")
    elif max_dd <= 0.08:
        score -= 8
        factors.append(f"Resilient price structure with low max drawdown ({max_dd*100:.1f}%).")
        
    # RSI Extreme impact
    if current_rsi >= 75:
        score += 10
        factors.append(f"Overbought conditions (RSI {current_rsi:.1f}) increase mean-reversion risk.")
    elif current_rsi <= 25:
        score += 10
        factors.append(f"Oversold territory (RSI {current_rsi:.1f}) indicates sharp recent selling pressure.")
    elif 40 <= current_rsi <= 60:
        score -= 5
        factors.append("RSI is balanced within the neutral healthy zone.")
        
    # Volume anomaly impact
    if volume_anomaly:
        score += 8
        factors.append(f"Volume surge detected ({vol_ratio:.1f}x 20-day average), indicating heightened institutional activity.")
        
    # Daily shock
    if daily_shock:
        score += 8
        factors.append(f"Sharp single-day price movement ({latest_return*100:.1f}%) observed.")
        
    # Clamp score to [5, 95]
    score = int(np.clip(score, 5, 95))
    
    if score <= 38:
        level = "LOW"
    elif score <= 68:
        level = "MODERATE"
    else:
        level = "HIGH"
        
    return {
        "ticker": ticker,
        "risk_score": score,
        "risk_level": level,
        "volatility_annualized": round(volatility, 4),
        "max_drawdown": round(max_dd, 4),
        "volume_anomaly": volume_anomaly,
        "rsi_extreme": rsi_extreme,
        "risk_factors": factors
    }
