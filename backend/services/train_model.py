import os
import joblib
import numpy as np
import pandas as pd
from typing import List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier

from backend.config import MODELS_DIR
from backend.services.market_data import get_stock_data
from backend.services.technical_analysis import calculate_indicators

FEATURE_COLUMNS = [
    "return_1d",
    "return_5d",
    "vol_ratio_5d",
    "rsi_14",
    "macd",
    "macd_signal",
    "macd_hist",
    "price_to_sma20",
    "price_to_sma50",
    "price_to_ema20",
    "bb_position",
    "volatility_20",
    "momentum_10",
]

def prepare_features_and_target(df: pd.DataFrame, forward_window: int = 5) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Computes normalized, stationary ML features and forward return target.
    Eliminates lookahead bias by strictly shifting target backwards.
    """
    data = calculate_indicators(df)
    close = data["Close"]
    volume = data["Volume"]
    
    features = pd.DataFrame(index=data.index)
    features["return_1d"] = data["Return"]
    features["return_5d"] = close.pct_change(5).fillna(0.0)
    
    vol_sma5 = volume.rolling(5, min_periods=1).mean()
    features["vol_ratio_5d"] = (volume / vol_sma5.replace(0, 1.0)).clip(0, 5)
    
    features["rsi_14"] = data["RSI_14"]
    features["macd"] = data["MACD"]
    features["macd_signal"] = data["MACD_Signal"]
    features["macd_hist"] = data["MACD_Hist"]
    
    features["price_to_sma20"] = (close / data["SMA_20"].replace(0, np.nan) - 1).fillna(0)
    features["price_to_sma50"] = (close / data["SMA_50"].replace(0, np.nan) - 1).fillna(0)
    features["price_to_ema20"] = (close / data["EMA_20"].replace(0, np.nan) - 1).fillna(0)
    
    bb_range = (data["BB_Upper"] - data["BB_Lower"]).replace(0, np.nan)
    features["bb_position"] = ((close - data["BB_Lower"]) / bb_range).fillna(0.5).clip(-0.5, 1.5)
    
    features["volatility_20"] = data["Volatility_20"]
    features["momentum_10"] = data["Momentum_10"]
    
    # Forward return target: return over next `forward_window` days
    future_close = close.shift(-forward_window)
    future_return = (future_close / close - 1)
    
    # Binary target: 1 if positive return, 0 otherwise
    target = (future_return > 0).astype(int)
    
    # Drop rows where target is NaN (the last forward_window rows) and initial rows with NaNs
    valid_idx = target.dropna().index[:-forward_window]
    
    return features.loc[valid_idx, FEATURE_COLUMNS], target.loc[valid_idx]

def extract_latest_feature_vector(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts features for the latest single timestamp to run inference."""
    data = calculate_indicators(df)
    close = data["Close"]
    volume = data["Volume"]
    
    features = pd.DataFrame(index=[data.index[-1]])
    features["return_1d"] = float(data["Return"].iloc[-1])
    features["return_5d"] = float(close.pct_change(5).fillna(0.0).iloc[-1])
    
    vol_sma5 = volume.rolling(5, min_periods=1).mean().iloc[-1]
    features["vol_ratio_5d"] = float(np.clip(volume.iloc[-1] / (vol_sma5 if vol_sma5 > 0 else 1.0), 0, 5))
    
    features["rsi_14"] = float(data["RSI_14"].iloc[-1])
    features["macd"] = float(data["MACD"].iloc[-1])
    features["macd_signal"] = float(data["MACD_Signal"].iloc[-1])
    features["macd_hist"] = float(data["MACD_Hist"].iloc[-1])
    
    sma20 = float(data["SMA_20"].iloc[-1])
    sma50 = float(data["SMA_50"].iloc[-1])
    ema20 = float(data["EMA_20"].iloc[-1])
    last_close = float(close.iloc[-1])
    
    features["price_to_sma20"] = (last_close / sma20 - 1) if sma20 else 0.0
    features["price_to_sma50"] = (last_close / sma50 - 1) if sma50 else 0.0
    features["price_to_ema20"] = (last_close / ema20 - 1) if ema20 else 0.0
    
    bb_range = float(data["BB_Upper"].iloc[-1] - data["BB_Lower"].iloc[-1])
    features["bb_position"] = float(np.clip((last_close - data["BB_Lower"].iloc[-1]) / (bb_range if bb_range > 0 else 1.0), -0.5, 1.5))
    
    features["volatility_20"] = float(data["Volatility_20"].iloc[-1])
    features["momentum_10"] = float(data["Momentum_10"].iloc[-1])
    
    return features[FEATURE_COLUMNS]

def train_and_save_model(tickers: List[str] = None) -> dict:
    """
    Gathers historical data across multiple bluechip stocks,
    splits chronologically, trains an XGBoost model, evaluates metrics,
    and saves the model artifact.
    """
    if tickers is None:
        tickers = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "AAPL", "MSFT"]
        
    print(f"Gathering data for training tickers: {tickers}...")
    all_X = []
    all_y = []
    
    for ticker in tickers:
        try:
            df, _ = get_stock_data(ticker, period="5y")
            if len(df) > 100:
                X, y = prepare_features_and_target(df)
                all_X.append(X)
                all_y.append(y)
                print(f"  [OK] {ticker}: {len(X)} feature rows prepared")
        except Exception as e:
            print(f"  [ERROR] Failed for {ticker}: {e}")
            
    if not all_X:
        raise ValueError("No training data could be collected.")
        
    combined_X = pd.concat(all_X).reset_index(drop=True)
    combined_y = pd.concat(all_y).reset_index(drop=True)
    
    # Chronological 80/20 train/test split
    split_idx = int(len(combined_X) * 0.80)
    X_train, X_test = combined_X.iloc[:split_idx], combined_X.iloc[split_idx:]
    y_train, y_test = combined_y.iloc[:split_idx], combined_y.iloc[split_idx:]
    
    print(f"Training XGBoost on {len(X_train)} samples, testing on {len(X_test)} samples...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)
    auc = roc_auc_score(y_test, probs)
    
    metrics = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(auc, 4),
        "test_samples": len(y_test)
    }
    print("Model Evaluation Metrics:")
    for k, v in metrics.items():
        print(f"  - {k}: {v}")
        
    # Save artifacts
    model_path = MODELS_DIR / "trend_model.pkl"
    features_path = MODELS_DIR / "feature_names.pkl"
    
    joblib.dump(model, model_path)
    joblib.dump(FEATURE_COLUMNS, features_path)
    print(f"Model successfully saved to {model_path}")
    print(f"Feature names saved to {features_path}")
    
    return metrics

if __name__ == "__main__":
    train_and_save_model()
