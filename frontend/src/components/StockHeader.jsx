import React from 'react';
import { ArrowUpRight, ArrowDownRight, Globe, BarChart2, Clock } from 'lucide-react';

export default function StockHeader({ stock }) {
  if (!stock) return null;

  const isPositive = stock.change >= 0;
  const currencySymbol = stock.currency === 'INR' ? '₹' : '$';

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 lg:p-6 shadow-xl relative overflow-hidden backdrop-blur-sm">
      {/* Background glow accent */}
      <div 
        className={`absolute -right-20 -top-20 w-64 h-64 rounded-full blur-3xl pointer-events-none opacity-15 ${
          isPositive ? 'bg-emerald-500' : 'bg-rose-500'
        }`} 
      />

      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
        
        {/* Left: Ticker & Company */}
        <div className="space-y-1.5">
          <div className="flex items-center gap-3">
            <span className="text-2xl lg:text-3xl font-extrabold tracking-tight text-white font-mono">
              {stock.ticker}
            </span>
            <span className="px-2.5 py-0.5 rounded-md bg-slate-800 border border-slate-700 text-xs font-semibold text-slate-300">
              {stock.exchange}
            </span>
            <span className="px-2 py-0.5 rounded-md bg-cyan-950/60 border border-cyan-800/60 text-[11px] font-mono text-cyan-400">
              {stock.currency}
            </span>
          </div>
          <h1 className="text-sm lg:text-base font-medium text-slate-400">
            {stock.company_name}
          </h1>
          <div className="flex items-center gap-2 text-xs text-slate-500 pt-1">
            <Clock className="w-3.5 h-3.5" />
            <span>Updated: {stock.timestamp}</span>
          </div>
        </div>

        {/* Middle: Live Price & Delta */}
        <div className="flex flex-col items-start lg:items-end space-y-1">
          <div className="text-3xl lg:text-4xl font-extrabold tracking-tight text-white font-mono">
            {currencySymbol}{stock.current_price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </div>
          <div className="flex items-center gap-2">
            <div className={`inline-flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-bold font-mono tracking-wide ${
              isPositive ? 'bg-emerald-950/80 text-emerald-400 border border-emerald-800/80' : 'bg-rose-950/80 text-rose-400 border border-rose-800/80'
            }`}>
              {isPositive ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
              <span>{isPositive ? '+' : ''}{stock.change.toFixed(2)} ({isPositive ? '+' : ''}{stock.change_percent.toFixed(2)}%)</span>
            </div>
            <span className="text-xs text-slate-500">Today</span>
          </div>
        </div>

        {/* Right: Key Stats Pills */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 lg:border-l lg:border-slate-800 lg:pl-6">
          <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-2.5">
            <div className="text-[11px] font-medium text-slate-400">Day High</div>
            <div className="text-sm font-semibold text-slate-200 font-mono mt-0.5">
              {currencySymbol}{stock.day_high ? stock.day_high.toFixed(2) : '-'}
            </div>
          </div>

          <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-2.5">
            <div className="text-[11px] font-medium text-slate-400">Day Low</div>
            <div className="text-sm font-semibold text-slate-200 font-mono mt-0.5">
              {currencySymbol}{stock.day_low ? stock.day_low.toFixed(2) : '-'}
            </div>
          </div>

          <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-2.5">
            <div className="text-[11px] font-medium text-slate-400">52W High</div>
            <div className="text-sm font-semibold text-emerald-400 font-mono mt-0.5">
              {currencySymbol}{stock.high_52w ? stock.high_52w.toFixed(2) : '-'}
            </div>
          </div>

          <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-2.5">
            <div className="text-[11px] font-medium text-slate-400">52W Low</div>
            <div className="text-sm font-semibold text-rose-400 font-mono mt-0.5">
              {currencySymbol}{stock.low_52w ? stock.low_52w.toFixed(2) : '-'}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
