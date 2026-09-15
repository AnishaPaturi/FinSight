from typing import Tuple

POPULAR_TICKERS = {
    # Indian Bluechips (NSE)
    "RELIANCE": {"name": "Reliance Industries Ltd.", "suffix": ".NS", "currency": "INR"},
    "TCS": {"name": "Tata Consultancy Services Ltd.", "suffix": ".NS", "currency": "INR"},
    "INFY": {"name": "Infosys Ltd.", "suffix": ".NS", "currency": "INR"},
    "HDFCBANK": {"name": "HDFC Bank Ltd.", "suffix": ".NS", "currency": "INR"},
    "ICICIBANK": {"name": "ICICI Bank Ltd.", "suffix": ".NS", "currency": "INR"},
    "SBIN": {"name": "State Bank of India", "suffix": ".NS", "currency": "INR"},
    "BHARTIARTL": {"name": "Bharti Airtel Ltd.", "suffix": ".NS", "currency": "INR"},
    "ITC": {"name": "ITC Ltd.", "suffix": ".NS", "currency": "INR"},
    "LT": {"name": "Larsen & Toubro Ltd.", "suffix": ".NS", "currency": "INR"},
    "TATAMOTORS": {"name": "Tata Motors Ltd.", "suffix": ".NS", "currency": "INR"},
    "WIPRO": {"name": "Wipro Ltd.", "suffix": ".NS", "currency": "INR"},
    "HINDUNILVR": {"name": "Hindustan Unilever Ltd.", "suffix": ".NS", "currency": "INR"},
    
    # US Tech & Global
    "AAPL": {"name": "Apple Inc.", "suffix": "", "currency": "USD"},
    "MSFT": {"name": "Microsoft Corporation", "suffix": "", "currency": "USD"},
    "GOOGL": {"name": "Alphabet Inc.", "suffix": "", "currency": "USD"},
    "NVDA": {"name": "NVIDIA Corporation", "suffix": "", "currency": "USD"},
    "AMZN": {"name": "Amazon.com Inc.", "suffix": "", "currency": "USD"},
    "TSLA": {"name": "Tesla Inc.", "suffix": "", "currency": "USD"},
    "META": {"name": "Meta Platforms Inc.", "suffix": "", "currency": "USD"},
}

def resolve_ticker(query: str) -> Tuple[str, str, str]:
    """
    Normalizes a user query/ticker string.
    Returns: (standard_ticker, yfinance_symbol, currency)
    Example: 'reliance' -> ('RELIANCE', 'RELIANCE.NS', 'INR')
             'aapl'     -> ('AAPL', 'AAPL', 'USD')
    """
    cleaned = query.strip().upper()
    
    # Check if suffix already provided
    if cleaned.endswith(".NS") or cleaned.endswith(".BO"):
        base = cleaned.split(".")[0]
        name = POPULAR_TICKERS.get(base, {}).get("name", cleaned)
        return base, cleaned, "INR"
    
    if cleaned in POPULAR_TICKERS:
        meta = POPULAR_TICKERS[cleaned]
        yf_symbol = cleaned + meta["suffix"]
        return cleaned, yf_symbol, meta["currency"]
    
    # If not in dictionary and looks like standard US ticker (3-5 letters)
    # Default to directly passing symbol, fallback will handle it
    return cleaned, cleaned, "USD"

def format_currency(value: float, currency: str = "INR") -> str:
    symbol = "₹" if currency == "INR" else "$"
    return f"{symbol}{value:,.2f}"

def format_percent(value: float) -> str:
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value:.2f}%"
