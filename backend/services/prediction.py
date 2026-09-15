import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any

from backend.config import MODELS_DIR
from backend.services.train_model import extract_latest_feature_vector, FEATURE_COLUMNS

_MODEL = None
_FEATURE_NAMES = None

def get_loaded_model():
    """Lazy loader for the trained ML model artifact."""
    global _MODEL, _FEATURE_NAMES
    if _MODEL is None:
        model_path = MODELS_DIR / "trend_model.pkl"
        features_path = MODELS_DIR / "feature_names.pkl"
        if model_path.exists():
            _MODEL = joblib.load(model_path)
            _FEATURE_NAMES = joblib.load(features_path) if features_path.exists() else FEATURE_COLUMNS
    return _MODEL, _FEATURE_NAMES

def predict_trend(df: pd.DataFrame, ticker: str) -> Dict[str, Any]:
    """
    Runs ML inference on the latest market features for the given stock.
    Returns trend direction ('BULLISH', 'BEARISH', 'NEUTRAL') and confidence.
    """
    if df.empty or len(df) < 20:
        return {
            "ticker": ticker,
            "prediction": "NEUTRAL",
            "confidence": 0.50,
            "probabilities": {"BULLISH": 0.50, "BEARISH": 0.50},
            "model_name": "Heuristic (Insufficient Data)",
            "features_used": {}
        }
        
    features_df = extract_latest_feature_vector(df)
    features_dict = {col: round(float(features_df[col].iloc[0]), 4) for col in features_df.columns}
    
    model, feature_names = get_loaded_model()
    
    if model is not None:
        try:
            # Ensure column order matches training
            cols_to_use = feature_names if feature_names else FEATURE_COLUMNS
            X_input = features_df[cols_to_use]
            
            prob_up = float(model.predict_proba(X_input)[0, 1])
            prob_down = 1.0 - prob_up
            
            if prob_up >= 0.55:
                prediction = "BULLISH"
                confidence = prob_up
            elif prob_up <= 0.45:
                prediction = "BEARISH"
                confidence = prob_down
            else:
                prediction = "NEUTRAL"
                confidence = max(prob_up, prob_down)
                
            return {
                "ticker": ticker,
                "prediction": prediction,
                "confidence": round(confidence, 2),
                "probabilities": {
                    "BULLISH": round(prob_up, 2),
                    "BEARISH": round(prob_down, 2)
                },
                "model_name": "XGBoost Trend Classifier",
                "features_used": features_dict
            }
        except Exception as e:
            print(f"Warning: Model inference error ({e}), falling back to quantitative heuristics.")
            
    # Heuristic quantitative trend rule if model artifact is unavailable
    rsi = features_dict.get("rsi_14", 50.0)
    macd_hist = features_dict.get("macd_hist", 0.0)
    price_to_sma20 = features_dict.get("price_to_sma20", 0.0)
    
    bullish_score = 0
    if rsi > 50: bullish_score += 1
    if macd_hist > 0: bullish_score += 1
    if price_to_sma20 > 0: bullish_score += 1
    
    if bullish_score >= 2:
        prediction = "BULLISH"
        confidence = 0.65
    elif bullish_score == 0:
        prediction = "BEARISH"
        confidence = 0.65
    else:
        prediction = "NEUTRAL"
        confidence = 0.52
        
    return {
        "ticker": ticker,
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "probabilities": {
            "BULLISH": round(confidence if prediction == "BULLISH" else 1 - confidence, 2),
            "BEARISH": round(confidence if prediction == "BEARISH" else 1 - confidence, 2)
        },
        "model_name": "Quantitative Composite Baseline",
        "features_used": features_dict
    }
