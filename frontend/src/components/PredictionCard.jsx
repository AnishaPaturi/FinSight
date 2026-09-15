import React from 'react';
import { BrainCircuit, Zap, CheckCircle2, AlertTriangle, HelpCircle } from 'lucide-react';

export default function PredictionCard({ prediction, technical }) {
  if (!prediction) return null;

  const isBullish = prediction.prediction === 'BULLISH';
  const isBearish = prediction.prediction === 'BEARISH';
  const confPct = Math.round(prediction.confidence * 100);

  const badgeColor = isBullish
    ? 'text-emerald-400 bg-emerald-950/70 border-emerald-700/60 shadow-emerald-500/10'
    : isBearish
    ? 'text-rose-400 bg-rose-950/70 border-rose-700/60 shadow-rose-500/10'
    : 'text-amber-400 bg-amber-950/70 border-amber-700/60 shadow-amber-500/10';

  const progressBg = isBullish
    ? 'bg-gradient-to-r from-emerald-500 to-teal-400'
    : isBearish
    ? 'bg-gradient-to-r from-rose-500 to-orange-400'
    : 'bg-gradient-to-r from-amber-500 to-yellow-400';

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden flex flex-col justify-between">
      {/* Glow accent */}
      <div className={`absolute top-0 right-0 w-32 h-32 blur-3xl opacity-20 pointer-events-none ${
        isBullish ? 'bg-emerald-500' : isBearish ? 'bg-rose-500' : 'bg-amber-500'
      }`} />

      <div>
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-cyan-950/60 text-cyan-400 border border-cyan-800/50">
              <BrainCircuit className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold tracking-wide text-slate-200 uppercase">
              AI Market Signal
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-500">5-Day Horizon</span>
        </div>

        {/* Signal Hero */}
        <div className="py-5 text-center">
          <div className="inline-block">
            <div className={`text-3xl font-black font-mono tracking-wider px-6 py-2 rounded-2xl border shadow-lg ${badgeColor}`}>
              {prediction.prediction}
            </div>
          </div>
          <div className="mt-3 flex items-center justify-center gap-1.5 text-slate-300 text-sm font-medium">
            <Zap className="w-4 h-4 text-cyan-400 fill-cyan-400" />
            <span>Confidence: <strong className="text-white font-mono">{confPct}%</strong></span>
          </div>

          {/* Confidence Meter Bar */}
          <div className="mt-3 w-full bg-slate-800/80 h-2 rounded-full overflow-hidden p-0.5 border border-slate-700/50">
            <div
              className={`h-full rounded-full transition-all duration-500 ${progressBg}`}
              style={{ width: `${confPct}%` }}
            />
          </div>
        </div>

        {/* Key Model Signals */}
        <div className="space-y-2 bg-slate-950/50 rounded-xl p-3 border border-slate-800/60 text-xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
            Contributing Quantitative Factors
          </div>
          <div className="flex items-center justify-between text-slate-300">
            <span>RSI Momentum (14):</span>
            <span className="font-mono font-medium text-slate-100">{technical?.rsi ?? '-'}</span>
          </div>
          <div className="flex items-center justify-between text-slate-300">
            <span>MACD Histogram:</span>
            <span className={`font-mono font-medium ${technical?.macd_hist >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {technical?.macd_hist ? technical.macd_hist.toFixed(2) : '-'}
            </span>
          </div>
          <div className="flex items-center justify-between text-slate-300">
            <span>Price vs SMA 20:</span>
            <span className={`font-mono font-medium ${technical?.current_price >= technical?.sma_20 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {technical?.current_price >= technical?.sma_20 ? 'Above (+)' : 'Below (-)'}
            </span>
          </div>
        </div>
      </div>

      {/* Footer disclaimer */}
      <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center gap-1.5 text-[10px] text-slate-500">
        <HelpCircle className="w-3.5 h-3.5 flex-shrink-0 text-slate-500" />
        <span>Model: {prediction.model_name}. Directional probability, not a price target.</span>
      </div>
    </div>
  );
}
