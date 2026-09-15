import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import StockHeader from './components/StockHeader';
import PriceChart from './components/PriceChart';
import TechnicalIndicators from './components/TechnicalIndicators';
import PredictionCard from './components/PredictionCard';
import SentimentCard from './components/SentimentCard';
import RiskCard from './components/RiskCard';
import AIReport from './components/AIReport';
import AskFinSight from './components/AskFinSight';
import { AlertCircle, RefreshCw, BarChart2 } from 'lucide-react';

export default function App() {
  const [ticker, setTicker] = useState('RELIANCE');
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAnalysis = async (tickerQuery) => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/full-analysis/${encodeURIComponent(tickerQuery)}`);
      if (!res.ok) {
        throw new Error(`Failed to load data for "${tickerQuery}". Verify the ticker symbol.`);
      }
      const json = await res.json();
      setData(json);
      setTicker(json.stock.ticker);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred while fetching analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis(ticker);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-cyan-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        onSearch={fetchAnalysis}
        currentTicker={ticker}
        isLoading={isLoading}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 space-y-6">
        
        {/* Error Alert */}
        {error && (
          <div className="bg-rose-950/70 border border-rose-800 rounded-2xl p-4 flex items-center justify-between text-rose-200 text-sm shadow-xl">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => fetchAnalysis(ticker)}
              className="px-3 py-1.5 rounded-lg bg-rose-900/60 hover:bg-rose-900 text-xs font-semibold text-white transition-all flex items-center gap-1"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        )}

        {/* Loading Skeleton */}
        {isLoading && !data && (
          <div className="space-y-6 animate-pulse">
            <div className="h-32 bg-slate-900/60 rounded-2xl border border-slate-800" />
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <div className="h-96 bg-slate-900/60 rounded-2xl border border-slate-800" />
                <div className="h-64 bg-slate-900/60 rounded-2xl border border-slate-800" />
              </div>
              <div className="space-y-6">
                <div className="h-64 bg-slate-900/60 rounded-2xl border border-slate-800" />
                <div className="h-64 bg-slate-900/60 rounded-2xl border border-slate-800" />
              </div>
            </div>
          </div>
        )}

        {/* Dashboard Content */}
        {data && (
          <div className="space-y-6">
            
            {/* 1. Header with Stock Price and Deltas */}
            <StockHeader stock={data.stock} />

            {/* 2. Main Dashboard Split Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              
              {/* Left Column (Primary Visuals & Deep Report - 7 cols) */}
              <div className="lg:col-span-7 space-y-6">
                <PriceChart
                  historical={data.historical}
                  currency={data.stock.currency}
                  technical={data.technical}
                />
                <TechnicalIndicators
                  technical={data.technical}
                  currency={data.stock.currency}
                />
                <AIReport report={data.ai_analysis} />
              </div>

              {/* Right Column (Signals, Sentiment, Risk, Router - 5 cols) */}
              <div className="lg:col-span-5 space-y-6">
                <PredictionCard
                  prediction={data.prediction}
                  technical={data.technical}
                />
                <SentimentCard sentiment={data.sentiment} />
                <RiskCard risk={data.risk} />
                <AskFinSight ticker={data.stock.ticker} />
              </div>

            </div>

          </div>
        )}

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/90 py-6 px-4 lg:px-8 mt-12 text-center text-xs text-slate-500 space-y-2">
        <p className="font-medium text-slate-400">
          FinSight — AI-Powered Stock Market Intelligence Platform
        </p>
        <p className="max-w-2xl mx-auto text-[11px] text-slate-600">
          Disclaimer: This system separates quantitative machine learning prediction from natural-language reasoning for research and educational purposes only. It does not provide guaranteed returns or investment advice.
        </p>
      </footer>
    </div>
  );
}
