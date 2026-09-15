from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.config import CORS_ORIGINS, PORT, HOST
from backend.api.stock import router as stock_router
from backend.api.news import router as news_router
from backend.api.analysis import router as analysis_router

app = FastAPI(
    title="FinSight Intelligence API",
    description="AI-Powered Stock Market Intelligence & Quantitative Analysis Platform",
    version="1.0.0"
)

# CORS Setup for Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(stock_router)
app.include_router(news_router)
app.include_router(analysis_router)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "platform": "FinSight",
        "description": "AI-Powered Stock Market Intelligence Platform",
        "endpoints": {
            "full_analysis": "/api/full-analysis/{ticker}",
            "stock_overview": "/api/stock/{ticker}",
            "historical_data": "/api/stock/{ticker}/history",
            "technical_indicators": "/api/technical/{ticker}",
            "ml_prediction": "/api/prediction/{ticker}",
            "sentiment_analysis": "/api/sentiment/{ticker}",
            "risk_analysis": "/api/risk/{ticker}",
            "ai_report": "/api/analysis/{ticker}",
            "interactive_chat": "/api/chat",
            "docs": "/docs"
        }
    }

# Mount built frontend static files if available
from pathlib import Path
from fastapi.staticfiles import StaticFiles

frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
else:
    @app.get("/", tags=["Health"])
    def root_health():
        return health_check()

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
