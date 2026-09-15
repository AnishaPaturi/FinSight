import React from 'react';
import { Activity, Gauge, Compass, Waves, SlidersHorizontal, BarChart } from 'lucide-react';

export default function TechnicalIndicators({ technical, currency = 'INR' }) {
  if (!technical) return null;

  const currencySymbol = currency === 'INR' ? '₹' : '$';
  const signals = technical.summary_signals || {};

  const getRsiColor = (rsi) => {
    if (rsi >= 70) return 'text-rose-400 border-rose-500/30 bg-rose-950/40';
    if (rsi <= 30) return 'text-emerald-400 border-emerald-500/30 bg-emerald-950/40';
    return 'text-cyan-400 border-cyan-500/30 bg-cyan-950/40';
  };

  const getMacdColor = (hist) => {
    return hist >= 0
      ? 'text-emerald-400 border-emerald-500/30 bg-emerald-950/40'
      : 'text-rose-400 border-rose-500/30 bg-rose-950/40';
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 lg:p-6 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <SlidersHorizontal className="w-5 h-5 text-cyan-400" />
          <h2 className="text-base font-bold text-slate-100 tracking-tight">Technical Indicators & Signals</h2>
        </div>
        <span className="text-xs text-slate-400 font-mono">14 & 20 Period Calibration</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Card 1: RSI */}
        <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">RSI (14)</span>
            <Gauge className="w-4 h-4 text-slate-500" />
          </div>
          <div className="my-2">
            <div className="text-2xl font-bold font-mono text-white">
              {technical.rsi ? technical.rsi.toFixed(1) : '-'}
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 via-cyan-400 to-rose-500"
                style={{ width: `${Math.min(Math.max(technical.rsi || 50, 0), 100)}%` }}
              />
            </div>
          </div>
          <div className={`text-[11px] font-medium px-2 py-1 rounded-md border text-center ${getRsiColor(technical.rsi)}`}>
            {signals.RSI || 'Neutral'}
          </div>
        </div>

        {/* Card 2: MACD */}
        <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">MACD (12, 26, 9)</span>
            <Activity className="w-4 h-4 text-slate-500" />
          </div>
          <div className="my-2">
            <div className="text-2xl font-bold font-mono text-white">
              {technical.macd ? technical.macd.toFixed(2) : '-'}
            </div>
            <div className="text-xs font-mono text-slate-400 mt-1 flex justify-between">
              <span>Sig: {technical.macd_signal ? technical.macd_signal.toFixed(2) : '-'}</span>
              <span className={technical.macd_hist >= 0 ? 'text-emerald-400' : 'text-rose-400'}>
                Hist: {technical.macd_hist ? technical.macd_hist.toFixed(2) : '-'}
              </span>
            </div>
          </div>
          <div className={`text-[11px] font-medium px-2 py-1 rounded-md border text-center ${getMacdColor(technical.macd_hist)}`}>
            {signals.MACD || 'Neutral'}
          </div>
        </div>

        {/* Card 3: Moving Averages */}
        <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Moving Averages</span>
            <Compass className="w-4 h-4 text-slate-500" />
          </div>
          <div className="my-2 space-y-1 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-amber-400 font-medium">SMA 20:</span>
              <span className="text-slate-200">{currencySymbol}{technical.sma_20 ? technical.sma_20.toFixed(2) : '-'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-indigo-400 font-medium">SMA 50:</span>
              <span className="text-slate-200">{currencySymbol}{technical.sma_50 ? technical.sma_50.toFixed(2) : '-'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-cyan-400 font-medium">EMA 20:</span>
              <span className="text-slate-200">{currencySymbol}{technical.ema_20 ? technical.ema_20.toFixed(2) : '-'}</span>
            </div>
          </div>
          <div className="text-[11px] font-medium px-2 py-1 rounded-md border text-center text-slate-300 bg-slate-900 border-slate-700 truncate">
            {signals.MovingAverages || 'Consolidating'}
          </div>
        </div>

        {/* Card 4: Bollinger Bands & Volatility */}
        <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Volatility & Bands</span>
            <Waves className="w-4 h-4 text-slate-500" />
          </div>
          <div className="my-2 space-y-1 text-xs font-mono">
            <div className="flex justify-between">
              <span className="text-slate-400">Ann. Volatility:</span>
              <span className="text-slate-100 font-semibold">{technical.volatility ? (technical.volatility * 100).toFixed(1) : '-'}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">BB Upper:</span>
              <span className="text-slate-300">{currencySymbol}{technical.bollinger_upper ? technical.bollinger_upper.toFixed(1) : '-'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">BB Lower:</span>
              <span className="text-slate-300">{currencySymbol}{technical.bollinger_lower ? technical.bollinger_lower.toFixed(1) : '-'}</span>
            </div>
          </div>
          <div className="text-[11px] font-medium px-2 py-1 rounded-md border text-center text-slate-300 bg-slate-900 border-slate-700 truncate">
            {signals.BollingerBands || 'Normal Band'}
          </div>
        </div>

      </div>
    </div>
  );
}
