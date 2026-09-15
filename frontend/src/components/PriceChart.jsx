import React, { useState, useMemo } from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Area,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';
import { Layers, Calendar, BarChart3 } from 'lucide-react';

const TIMEFRAMES = [
  { label: '1M', days: 22 },
  { label: '3M', days: 65 },
  { label: '6M', days: 130 },
  { label: '1Y', days: 252 },
  { label: 'ALL', days: 9999 }
];

export default function PriceChart({ historical, currency = 'INR', technical }) {
  const [selectedTf, setSelectedTf] = useState('6M');
  const [showSma20, setShowSma20] = useState(true);
  const [showSma50, setShowSma50] = useState(true);

  // Compute filtered series with rolling SMAs for charting
  const chartData = useMemo(() => {
    if (!historical || historical.length === 0) return [];

    const tf = TIMEFRAMES.find((t) => t.label === selectedTf);
    const sliceDays = tf ? tf.days : 130;
    const rawData = historical.slice(-sliceDays);

    // Compute rolling 20 & 50 SMAs over the sliced data
    return rawData.map((item, idx, arr) => {
      let sma20 = null;
      if (idx >= 19) {
        const sum20 = arr.slice(idx - 19, idx + 1).reduce((acc, curr) => acc + curr.close, 0);
        sma20 = Math.round((sum20 / 20) * 100) / 100;
      }

      let sma50 = null;
      if (idx >= 49) {
        const sum50 = arr.slice(idx - 49, idx + 1).reduce((acc, curr) => acc + curr.close, 0);
        sma50 = Math.round((sum50 / 50) * 100) / 100;
      }

      return {
        ...item,
        sma20,
        sma50
      };
    });
  }, [historical, selectedTf]);

  if (!chartData || chartData.length === 0) {
    return (
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 h-96 flex items-center justify-center text-slate-500">
        Loading price history...
      </div>
    );
  }

  const currencySymbol = currency === 'INR' ? '₹' : '$';
  const minPrice = Math.min(...chartData.map((d) => d.close));
  const maxPrice = Math.max(...chartData.map((d) => d.close));
  const yDomain = [Math.floor(minPrice * 0.96), Math.ceil(maxPrice * 1.04)];

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 lg:p-6 shadow-xl relative backdrop-blur-sm">
      {/* Chart Controls Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-5 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-cyan-400" />
          <h2 className="text-base font-bold text-slate-100 tracking-tight">Price Trend & Moving Averages</h2>
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
          {/* Indicator Toggles */}
          <div className="flex items-center gap-2 text-xs">
            <button
              onClick={() => setShowSma20(!showSma20)}
              className={`px-2.5 py-1 rounded-md font-mono border transition-all ${
                showSma20
                  ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                  : 'bg-slate-800/40 text-slate-500 border-slate-700/40'
              }`}
            >
              SMA 20
            </button>
            <button
              onClick={() => setShowSma50(!showSma50)}
              className={`px-2.5 py-1 rounded-md font-mono border transition-all ${
                showSma50
                  ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
                  : 'bg-slate-800/40 text-slate-500 border-slate-700/40'
              }`}
            >
              SMA 50
            </button>
          </div>

          {/* Timeframe Chips */}
          <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
            {TIMEFRAMES.map((tf) => (
              <button
                key={tf.label}
                onClick={() => setSelectedTf(tf.label)}
                className={`px-2 py-1 rounded-md font-medium transition-all ${
                  selectedTf === tf.label
                    ? 'bg-cyan-600 text-white font-semibold shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                {tf.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Chart */}
      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
            <defs>
              <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00b4d8" stopOpacity={0.35} />
                <stop offset="95%" stopColor="#00b4d8" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis
              dataKey="date"
              stroke="#64748b"
              fontSize={11}
              tickLine={false}
              tickFormatter={(str) => {
                const parts = str.split('-');
                return parts.length >= 3 ? `${parts[1]}/${parts[2]}` : str;
              }}
            />
            <YAxis
              domain={yDomain}
              stroke="#64748b"
              fontSize={11}
              tickLine={false}
              orientation="right"
              tickFormatter={(v) => `${currencySymbol}${v}`}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload;
                  return (
                    <div className="bg-slate-950 border border-slate-700 rounded-xl p-3 shadow-2xl text-xs space-y-1">
                      <div className="text-slate-400 font-mono pb-1 border-b border-slate-800">{label}</div>
                      <div className="text-slate-100 font-semibold font-mono">
                        Close: <span className="text-cyan-400">{currencySymbol}{data.close}</span>
                      </div>
                      <div className="text-slate-400 font-mono">
                        Vol: {(data.volume / 1_000_000).toFixed(2)}M
                      </div>
                      {data.sma20 && (
                        <div className="text-amber-400 font-mono">
                          SMA20: {currencySymbol}{data.sma20}
                        </div>
                      )}
                      {data.sma50 && (
                        <div className="text-indigo-400 font-mono">
                          SMA50: {currencySymbol}{data.sma50}
                        </div>
                      )}
                    </div>
                  );
                }
                return null;
              }}
            />
            <Area
              type="monotone"
              dataKey="close"
              name="Price"
              stroke="#00b4d8"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#priceGradient)"
            />
            {showSma20 && (
              <Line
                type="monotone"
                dataKey="sma20"
                name="SMA 20"
                stroke="#f59e0b"
                strokeWidth={1.5}
                dot={false}
              />
            )}
            {showSma50 && (
              <Line
                type="monotone"
                dataKey="sma50"
                name="SMA 50"
                stroke="#6366f1"
                strokeWidth={1.5}
                dot={false}
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
