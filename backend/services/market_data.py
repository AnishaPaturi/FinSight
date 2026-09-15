import datetime
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
import yfinance as yf

from backend.utils.helpers import resolve_ticker, POPULAR_TICKERS

def clean_yfinance_df(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten columns if multi-indexed, ensure index is Datetime and sort."""
    if df.empty:
        return df
    
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]
        
    df = df.reset_index()
    
    # Rename standard columns to Title case
    rename_dict = {}
    for col in df.columns:
        c_lower = str(col).lower()
        if "date" in c_lower:
            rename_dict[col] = "Date"
        elif "open" in c_lower:
            rename_dict[col] = "Open"
        elif "high" in c_lower:
            rename_dict[col] = "High"
        elif "low" in c_lower:
            rename_dict[col] = "Low"
        elif "close" in c_lower:
            rename_dict[col] = "Close"
        elif "volume" in c_lower:
            rename_dict[col] = "Volume"
            
    df = df.rename(columns=rename_dict)
    
    # Ensure required columns exist
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col not in df.columns and "Close" in df.columns:
            df[col] = df["Close"]
            
    # Clean datetime format
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        
    df = df.dropna(subset=["Close"]).sort_values("Date").reset_index(drop=True)
    return df

def generate_mock_stock_data(ticker: str, days: int = 500) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Generates synthetic stock data for offline testing and fallback."""
    np.random.seed(abs(hash(ticker)) % 10000)
    end_date = datetime.date.today()
    date_range = pd.date_range(end=end_date, periods=days, freq="B")
    
    base_price = 2500.0 if ticker in ["RELIANCE", "TCS"] else 1500.0
    returns = np.random.normal(0.0005, 0.018, size=len(date_range))
    price_series = base_price * np.cumprod(1 + returns)
    
    opens = price_series * (1 + np.random.normal(0, 0.004, size=len(date_range)))
    highs = np.maximum(opens, price_series) * (1 + np.abs(np.random.normal(0, 0.008, size=len(date_range))))
    lows = np.minimum(opens, price_series) * (1 - np.abs(np.random.normal(0, 0.008, size=len(date_range))))
    volumes = np.random.randint(1_000_000, 15_000_000, size=len(date_range))
    
    df = pd.DataFrame({
        "Date": date_range.strftime("%Y-%m-%d"),
        "Open": np.round(opens, 2),
        "High": np.round(highs, 2),
        "Low": np.round(lows, 2),
        "Close": np.round(price_series, 2),
        "Volume": volumes
    })
    
    current_price = float(df["Close"].iloc[-1])
    prev_price = float(df["Close"].iloc[-2])
    change = current_price - prev_price
    change_pct = (change / prev_price) * 100
    
    company_name = POPULAR_TICKERS.get(ticker, {}).get("name", f"{ticker} Corporation")
    currency = POPULAR_TICKERS.get(ticker, {}).get("currency", "INR")
    
    overview = {
        "ticker": ticker,
        "company_name": company_name,
        "current_price": round(current_price, 2),
        "change": round(change, 2),
        "change_percent": round(change_pct, 2),
        "currency": currency,
        "exchange": "NSE" if currency == "INR" else "NASDAQ",
        "day_high": round(float(df["High"].iloc[-1]), 2),
        "day_low": round(float(df["Low"].iloc[-1]), 2),
        "high_52w": round(float(df["High"].max()), 2),
        "low_52w": round(float(df["Low"].min()), 2),
        "market_cap": round(current_price * 1_000_000_000, 2),
        "pe_ratio": 24.5,
        "volume": int(df["Volume"].iloc[-1]),
        "avg_volume": int(df["Volume"].mean()),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return df, overview

def get_stock_data(query: str, period: str = "2y", interval: str = "1d") -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Downloads historical market data and metadata for a given ticker or query.
    Falls back gracefully to alternates or synthetic cache if needed.
    """
    std_ticker, yf_symbol, currency = resolve_ticker(query)
    
    symbols_to_try = [yf_symbol]
    if not yf_symbol.endswith(".NS") and currency == "INR":
        symbols_to_try.append(f"{std_ticker}.NS")
    if yf_symbol.endswith(".NS"):
        symbols_to_try.append(std_ticker)
        
    df = pd.DataFrame()
    ticker_obj = None
    successful_sym = yf_symbol
    
    for sym in symbols_to_try:
        try:
            t = yf.Ticker(sym)
            hist = t.history(period=period, interval=interval)
            if not hist.empty and len(hist) > 10:
                df = clean_yfinance_df(hist)
                ticker_obj = t
                successful_sym = sym
                break
        except Exception:
            continue
            
    if df.empty or len(df) < 5:
        # Graceful fallback to synthetic data
        return generate_mock_stock_data(std_ticker)
        
    # Extract metadata
    info: Dict[str, Any] = {}
    try:
        info = ticker_obj.fast_info or {}
    except Exception:
        pass
        
    current_price = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 else current_price
    change = current_price - prev_close
    change_pct = (change / prev_close) * 100 if prev_close else 0.0
    
    # Try fetching detailed name
    company_name = POPULAR_TICKERS.get(std_ticker, {}).get("name")
    if not company_name:
        try:
            full_info = ticker_obj.info
            company_name = full_info.get("shortName") or full_info.get("longName") or std_ticker
        except Exception:
            company_name = f"{std_ticker} Inc."
            
    day_high = float(df["High"].iloc[-1])
    day_low = float(df["Low"].iloc[-1])
    high_52w = float(df["High"].tail(252).max()) if len(df) >= 252 else float(df["High"].max())
    low_52w = float(df["Low"].tail(252).min()) if len(df) >= 252 else float(df["Low"].min())
    
    vol = int(df["Volume"].iloc[-1])
    avg_vol = int(df["Volume"].tail(30).mean())
    
    overview = {
        "ticker": std_ticker,
        "company_name": company_name,
        "current_price": round(current_price, 2),
        "change": round(change, 2),
        "change_percent": round(change_pct, 2),
        "currency": currency,
        "exchange": "NSE" if ".NS" in successful_sym or currency == "INR" else "US",
        "day_high": round(day_high, 2),
        "day_low": round(day_low, 2),
        "high_52w": round(high_52w, 2),
        "low_52w": round(low_52w, 2),
        "market_cap": getattr(info, "market_cap", None),
        "pe_ratio": None,
        "volume": vol,
        "avg_volume": avg_vol,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return df, overview
