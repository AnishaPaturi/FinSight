import React from 'react';
import { ShieldAlert, AlertOctagon, TrendingDown, Activity, CheckCircle } from 'lucide-react';

export default function RiskCard({ risk }) {
  if (!risk) return null;

  const isHigh = risk.risk_level === 'HIGH';
  const isLow = risk.risk_level === 'LOW';

  const badgeColor = isHigh
    ? 'text-rose-400 bg-rose-950/70 border-rose-700/60'
    : isLow
    ? 'text-emerald-400 bg-emerald-950/70 border-emerald-700/60'
    : 'text-amber-400 bg-amber-950/70 border-amber-700/60';

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 lg:p-6 shadow-xl backdrop-blur-sm flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-rose-950/60 text-rose-400 border border-rose-800/50">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold tracking-wide text-slate-200 uppercase">
              Risk Profile & Volatility
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-500">Multi-Factor Score</span>
        </div>

        {/* Score & Gauge */}
        <div className="py-4 flex items-center justify-between gap-4">
          <div>
            <div className="text-xs text-slate-400">Risk Assessment</div>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold font-mono text-white">
                {risk.risk_score}
              </span>
              <span className="text-xs text-slate-500 font-mono">/ 100</span>
              <span className={`text-xs font-bold px-2.5 py-0.5 rounded-lg border font-mono ml-2 ${badgeColor}`}>
                {risk.risk_level}
              </span>
            </div>
          </div>

          {/* Key Quantitative Metrics */}
          <div className="space-y-1 text-right text-xs font-mono">
            <div className="text-slate-300">
              Max Drawdown: <span className="text-rose-400 font-semibold font-mono">{(risk.max_drawdown * 100).toFixed(1)}%</span>
            </div>
            <div className="text-slate-300">
              Volatility: <span className="text-slate-100 font-semibold font-mono">{(risk.volatility_annualized * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>

        {/* Risk meter */}
        <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden relative border border-slate-700/50">
          <div
            className="h-full bg-gradient-to-r from-emerald-500 via-amber-500 to-rose-500 transition-all duration-500"
            style={{ width: `${risk.risk_score}%` }}
          />
        </div>

        {/* Risk Factors List */}
        <div className="mt-5 space-y-2">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Risk & Mitigation Factors
          </div>
          {risk.risk_factors.map((factor, idx) => (
            <div
              key={idx}
              className="flex items-start gap-2 bg-slate-950/60 border border-slate-800/70 rounded-xl p-2.5 text-xs text-slate-300"
            >
              {isHigh ? (
                <AlertOctagon className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
              ) : (
                <CheckCircle className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
              )}
              <span>{factor}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
