import React from 'react';
import { Newspaper, ExternalLink, ThumbsUp, ThumbsDown, Minus } from 'lucide-react';

export default function SentimentCard({ sentiment }) {
  if (!sentiment) return null;

  const isPos = sentiment.overall_sentiment === 'Positive';
  const isNeg = sentiment.overall_sentiment === 'Negative';

  const badgeColor = isPos
    ? 'text-emerald-400 bg-emerald-950/70 border-emerald-700/60'
    : isNeg
    ? 'text-rose-400 bg-rose-950/70 border-rose-700/60'
    : 'text-slate-300 bg-slate-800/70 border-slate-700/60';

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 lg:p-6 shadow-xl backdrop-blur-sm flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-sky-950/60 text-sky-400 border border-sky-800/50">
              <Newspaper className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold tracking-wide text-slate-200 uppercase">
              Financial News Sentiment
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-500">{sentiment.article_count} Sources</span>
        </div>

        {/* Overall Sentiment Metric */}
        <div className="py-4 flex items-center justify-between gap-4">
          <div>
            <div className="text-xs text-slate-400">Market Consensus</div>
            <div className="flex items-center gap-2 mt-1">
              <span className={`text-xl font-bold px-3 py-1 rounded-xl border font-mono ${badgeColor}`}>
                {sentiment.overall_sentiment}
              </span>
              <span className="text-xs text-slate-400 font-mono">
                Score: <strong className="text-white">{sentiment.overall_score > 0 ? '+' : ''}{sentiment.overall_score}</strong>
              </span>
            </div>
          </div>

          {/* Mini breakdown chips */}
          <div className="flex gap-1.5 text-[11px] font-mono">
            <span className="px-2 py-1 rounded-lg bg-emerald-950/60 text-emerald-400 border border-emerald-800/50">
              +{sentiment.positive_pct}%
            </span>
            <span className="px-2 py-1 rounded-lg bg-slate-800 text-slate-300 border border-slate-700/50">
              {sentiment.neutral_pct}%
            </span>
            <span className="px-2 py-1 rounded-lg bg-rose-950/60 text-rose-400 border border-rose-800/50">
              -{sentiment.negative_pct}%
            </span>
          </div>
        </div>

        {/* Proportional Sentiment Bar */}
        <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden flex my-2 border border-slate-700/50">
          <div style={{ width: `${sentiment.positive_pct}%` }} className="bg-emerald-500 h-full" title="Positive" />
          <div style={{ width: `${sentiment.neutral_pct}%` }} className="bg-slate-400 h-full" title="Neutral" />
          <div style={{ width: `${sentiment.negative_pct}%` }} className="bg-rose-500 h-full" title="Negative" />
        </div>

        {/* Recent Articles Stream */}
        <div className="mt-4 space-y-2.5">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Latest Headlines & NLP Classification
          </div>
          {sentiment.articles.slice(0, 3).map((art, idx) => (
            <div
              key={idx}
              className="bg-slate-950/60 border border-slate-800/70 rounded-xl p-3 hover:border-slate-700 transition-all text-xs"
            >
              <div className="flex items-start justify-between gap-2">
                <a
                  href={art.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-medium text-slate-200 hover:text-cyan-400 transition-colors line-clamp-2"
                >
                  {art.title}
                </a>
                <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border flex-shrink-0 font-mono ${
                  art.sentiment === 'Positive'
                    ? 'text-emerald-400 bg-emerald-950/60 border-emerald-800/60'
                    : art.sentiment === 'Negative'
                    ? 'text-rose-400 bg-rose-950/60 border-rose-800/60'
                    : 'text-slate-400 bg-slate-900 border-slate-700'
                }`}>
                  {art.sentiment}
                </span>
              </div>
              <div className="flex items-center justify-between text-[10px] text-slate-500 mt-2 font-mono">
                <span>{art.source}</span>
                <span>{art.published_at}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
