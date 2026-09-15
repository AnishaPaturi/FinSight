import React from 'react';
import { FileText, Sparkles, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function AIReport({ report }) {
  if (!report) return null;

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 lg:p-8 shadow-xl backdrop-blur-sm space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-cyan-600 to-sky-500 text-white shadow-md shadow-cyan-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">AI Intelligence & Synthesis Report</h2>
            <p className="text-xs text-slate-400">Multi-factor evidence synthesis for research and educational purposes</p>
          </div>
        </div>
        <span className="hidden sm:inline-block px-3 py-1 rounded-full text-xs font-semibold bg-cyan-950/60 text-cyan-400 border border-cyan-800/60">
          Synthesized by FinSight Engine
        </span>
      </div>

      {/* Executive Summary */}
      <div className="bg-slate-950/80 border border-slate-800/80 rounded-xl p-4 lg:p-5">
        <h3 className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-2 font-mono">
          Executive Summary
        </h3>
        <p className="text-sm text-slate-200 leading-relaxed font-sans">
          {report.executive_summary}
        </p>
      </div>

      {/* Grid: Technical vs Sentiment vs Risk */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div className="bg-slate-950/60 border border-slate-800/70 rounded-xl p-4">
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 font-mono">
            Technical Analysis
          </h4>
          <p className="text-xs text-slate-300 leading-relaxed">
            {report.technical_analysis}
          </p>
        </div>

        <div className="bg-slate-950/60 border border-slate-800/70 rounded-xl p-4">
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 font-mono">
            Market Sentiment
          </h4>
          <p className="text-xs text-slate-300 leading-relaxed">
            {report.market_sentiment}
          </p>
        </div>

        <div className="bg-slate-950/60 border border-slate-800/70 rounded-xl p-4">
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 font-mono">
            Risk & Drawdown
          </h4>
          <p className="text-xs text-slate-300 leading-relaxed">
            {report.risk_analysis}
          </p>
        </div>

      </div>

      {/* Drivers: Positive vs Negative Factors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        {/* Positive Factors */}
        <div className="bg-slate-950/60 border border-emerald-900/40 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 font-mono">
              Key Positive Factors
            </h4>
          </div>
          <ul className="space-y-2 text-xs text-slate-300">
            {report.positive_factors.map((factor, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-400 font-bold">•</span>
                <span>{factor}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Negative / Risk Factors */}
        <div className="bg-slate-950/60 border border-rose-900/40 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-rose-400 font-mono">
              Key Negative / Risk Factors
            </h4>
          </div>
          <ul className="space-y-2 text-xs text-slate-300">
            {report.negative_factors.map((factor, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-rose-400 font-bold">•</span>
                <span>{factor}</span>
              </li>
            ))}
          </ul>
        </div>

      </div>

      {/* Overall Outlook */}
      <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-4">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5 font-mono">
          Strategic Outlook
        </h4>
        <p className="text-xs text-slate-300 leading-relaxed">
          {report.overall_outlook}
        </p>
      </div>

      {/* Educational Disclaimer */}
      <div className="pt-2 border-t border-slate-800/80 flex items-start gap-2 text-[11px] text-slate-500 italic">
        <ShieldCheck className="w-4 h-4 text-slate-500 flex-shrink-0 mt-0.5" />
        <span>{report.disclaimer}</span>
      </div>

    </div>
  );
}
