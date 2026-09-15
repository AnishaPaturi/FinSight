from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StockOverview(BaseModel):
    ticker: str
    company_name: str
    current_price: float
    change: float
    change_percent: float
    currency: str = "INR"
    exchange: str = "NSE"
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    volume: Optional[int] = None
    avg_volume: Optional[int] = None
    timestamp: str

class PricePoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class HistoricalDataResponse(BaseModel):
    ticker: str
    company_name: str
    count: int
    prices: List[PricePoint]

class TechnicalIndicatorsResponse(BaseModel):
    ticker: str
    current_price: float
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    ema_20: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_hist: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_middle: Optional[float] = None
    bollinger_lower: Optional[float] = None
    volatility: Optional[float] = None
    daily_return: Optional[float] = None
    summary_signals: Dict[str, str] = Field(default_factory=dict)

class PredictionResponse(BaseModel):
    ticker: str
    prediction: str # BULLISH, BEARISH, NEUTRAL
    confidence: float # 0.0 to 1.0
    probabilities: Dict[str, float] = Field(default_factory=dict)
    model_name: str
    features_used: Dict[str, Any] = Field(default_factory=dict)

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = ""
    source: Optional[str] = ""
    published_at: Optional[str] = ""
    url: Optional[str] = ""
    sentiment: str # Positive, Neutral, Negative
    sentiment_score: float # -1.0 to 1.0

class SentimentResponse(BaseModel):
    ticker: str
    overall_sentiment: str # Positive, Neutral, Negative
    overall_score: float # -1.0 to 1.0
    positive_pct: float
    neutral_pct: float
    negative_pct: float
    article_count: int
    articles: List[NewsArticle]

class RiskResponse(BaseModel):
    ticker: str
    risk_score: int # 0 to 100
    risk_level: str # LOW, MODERATE, HIGH
    volatility_annualized: float
    max_drawdown: float
    volume_anomaly: bool
    rsi_extreme: bool
    risk_factors: List[str]

class AIAnalysisResponse(BaseModel):
    ticker: str
    executive_summary: str
    technical_analysis: str
    market_sentiment: str
    risk_analysis: str
    positive_factors: List[str]
    negative_factors: List[str]
    overall_outlook: str
    disclaimer: str = (
        "FinSight provides AI-generated information for educational and "
        "research purposes only and does not constitute financial advice."
    )

class FullAnalysisResponse(BaseModel):
    stock: StockOverview
    historical: List[PricePoint]
    technical: TechnicalIndicatorsResponse
    prediction: PredictionResponse
    sentiment: SentimentResponse
    risk: RiskResponse
    ai_analysis: AIAnalysisResponse
