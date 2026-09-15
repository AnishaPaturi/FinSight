import React, { useState } from 'react';
import { MessageSquare, Send, Bot, User, Route, Sparkles } from 'lucide-react';

const SUGGESTIONS = [
  'Why is this stock considered risky?',
  'What is the current RSI and momentum?',
  'Is the trend bullish or bearish?',
  'What are news headlines saying about the company?'
];

export default function AskFinSight({ ticker }) {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: `Hello! I'm FinSight AI. Ask me any quantitative, trend, sentiment, or risk question about ${ticker}.`,
      route: 'System Router'
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (queryText) => {
    const q = queryText || question;
    if (!q.trim() || isLoading) return;

    // Add user message
    const userMsg = { sender: 'user', text: q };
    setMessages((prev) => [...prev, userMsg]);
    setQuestion('');
    setIsLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, question: q })
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: data.answer,
          route: data.route_used
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'bot',
          text: 'Unable to reach the analysis router. Please check your network connection.',
          route: 'Error'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 lg:p-6 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-indigo-950/60 text-indigo-400 border border-indigo-800/50">
            <MessageSquare className="w-4 h-4" />
          </div>
          <h3 className="text-sm font-semibold tracking-wide text-slate-200 uppercase">
            Ask FinSight (Intelligent Model Router)
          </h3>
        </div>
        <span className="text-[11px] font-mono text-cyan-400">Dynamic Multi-Engine Routing</span>
      </div>

      {/* Suggested Questions */}
      <div className="py-3 flex flex-wrap gap-2">
        {SUGGESTIONS.map((s, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(s)}
            className="text-xs bg-slate-950/70 hover:bg-slate-800 text-slate-300 hover:text-white px-2.5 py-1 rounded-lg border border-slate-800 transition-all text-left"
          >
            {s}
          </button>
        ))}
      </div>

      {/* Chat Messages Log */}
      <div className="space-y-3 max-h-64 overflow-y-auto pr-1 my-2">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-xl px-3.5 py-2.5 text-xs leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-cyan-600 text-white font-medium'
                  : 'bg-slate-950/80 border border-slate-800 text-slate-200'
              }`}
            >
              {m.text}
            </div>
            {m.route && (
              <div className="flex items-center gap-1 text-[10px] text-slate-500 font-mono mt-1 px-1">
                <Route className="w-3 h-3 text-cyan-400" />
                <span>Routed via: {m.route}</span>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 text-xs text-slate-400 pl-2">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
            <span>Classifying query and synthesizing response...</span>
          </div>
        )}
      </div>

      {/* Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="mt-3 flex gap-2"
      >
        <input
          type="text"
          placeholder={`Ask about ${ticker}'s technicals, trend, news, or risk...`}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition-all"
        />
        <button
          type="submit"
          disabled={isLoading || !question.trim()}
          className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 text-white px-3.5 py-2 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all"
        >
          <Send className="w-3.5 h-3.5" />
          <span>Ask</span>
        </button>
      </form>
    </div>
  );
}
