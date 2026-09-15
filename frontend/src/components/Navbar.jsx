import React, { useState } from 'react';
import { Search, TrendingUp, Cpu, Activity, Sparkles } from 'lucide-react';

const QUICK_TICKERS = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'AAPL', 'NVDA'];

export default function Navbar({ onSearch, currentTicker, isLoading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Brand */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-start">
          <div className="flex items-center gap-2.5">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-600 via-sky-500 to-indigo-500 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <TrendingUp className="h-5 w-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold tracking-tight text-white font-mono">FIN<span className="text-cyan-400">SIGHT</span></span>
                <span className="text-[10px] uppercase font-semibold tracking-wider px-2 py-0.5 rounded-full bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">AI Intelligence</span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">Quantitative Market Research & Multi-Factor Signals</p>
            </div>
          </div>

          <div className="flex items-center gap-2 md:hidden">
            <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-emerald-400 font-medium">Live</span>
          </div>
        </div>

        {/* Search Bar */}
        <div className="w-full md:max-w-md">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="text"
              placeholder="Search ticker (e.g. RELIANCE, TCS, AAPL)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl pl-10 pr-24 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all shadow-inner"
            />
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
            <button
              type="submit"
              disabled={isLoading}
              className="absolute right-1.5 top-1.5 bottom-1.5 px-3 bg-cyan-600 hover:bg-cyan-500 active:scale-95 disabled:opacity-50 text-white rounded-lg text-xs font-semibold tracking-wide transition-all flex items-center gap-1 shadow-sm"
            >
              {isLoading ? (
                <span className="animate-spin h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full" />
              ) : (
                'Analyze'
              )}
            </button>
          </form>
        </div>

        {/* Quick Tickers & Live Status */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-between md:justify-end overflow-x-auto pb-1 md:pb-0">
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <span className="hidden lg:inline text-slate-500 mr-1">Popular:</span>
            {QUICK_TICKERS.map((t) => (
              <button
                key={t}
                onClick={() => onSearch(t)}
                className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-all ${
                  currentTicker === t
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold'
                    : 'bg-slate-800/60 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700/50'
                }`}
              >
                {t}
              </button>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-2 pl-2 border-l border-slate-800">
            <span className="flex h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-emerald-400 font-medium">Model v1.0</span>
          </div>
        </div>

      </div>
    </header>
  );
}
