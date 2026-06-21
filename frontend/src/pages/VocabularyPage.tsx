import React, { useState, useEffect } from 'react';
import { apiService, SignItem } from '../services/api';
import { Search, BookOpen, Sparkles, Lightbulb } from 'lucide-react';

export const VocabularyPage: React.FC = () => {
  const [signs, setSigns] = useState<SignItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [activeCategory, setActiveCategory] = useState<string>('all');

  useEffect(() => {
    async function loadSigns() {
      try {
        setLoading(true);
        const data = await apiService.getVocabulary();
        setSigns(data);
      } catch (err) {
        console.error('Failed to load vocabulary:', err);
      } finally {
        setLoading(false);
      }
    }
    loadSigns();
  }, []);

  const filteredSigns = signs.filter((sign) => {
    const matchesSearch =
      sign.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
      sign.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (sign.description && sign.description.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesCategory =
      activeCategory === 'all' || sign.category.toLowerCase() === activeCategory.toLowerCase();

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-slate-900 border border-slate-800">
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <BookOpen className="h-5 w-5 text-emerald-400" />
            <h2 className="text-xl font-bold text-white">Sign Language Word Dictionary & Reference</h2>
          </div>
          <p className="text-xs text-slate-400">
            Learn and reference all supported word signs, hand configurations, and communication controls.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative min-w-[280px]">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search words, actions, tips..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-950 border border-slate-800 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
        {[
          { id: 'all', label: 'All Signs' },
          { id: 'word', label: 'Words & Phrases' },
          { id: 'control', label: 'Control Actions' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveCategory(tab.id)}
            className={`px-4 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              activeCategory === tab.id
                ? 'bg-emerald-500 text-slate-950'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Loading Skeleton */}
      {loading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="h-44 rounded-2xl bg-slate-900/50 animate-pulse border border-slate-800" />
          ))}
        </div>
      )}

      {/* Signs Grid */}
      {!loading && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredSigns.map((sign) => (
            <div
              key={sign.id}
              className="bg-slate-900 border border-slate-800 hover:border-emerald-500/40 rounded-2xl p-4 shadow-lg flex flex-col justify-between transition-all hover:shadow-emerald-500/5"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xl font-black font-mono text-emerald-400">
                    {sign.symbol}
                  </span>
                  <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-md bg-slate-800 text-slate-300">
                    {sign.category}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-slate-100 mb-1">{sign.label}</h3>
                <p className="text-xs text-slate-400 leading-relaxed line-clamp-3">
                  {sign.description || 'No description provided.'}
                </p>
              </div>

              {sign.tips && (
                <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-start space-x-1.5 text-[11px] text-cyan-400">
                  <Lightbulb className="h-3.5 w-3.5 mt-0.5 shrink-0 text-cyan-400" />
                  <span>{sign.tips}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {!loading && filteredSigns.length === 0 && (
        <div className="text-center py-12 text-slate-500">
          <Sparkles className="h-8 w-8 mx-auto mb-2 opacity-40" />
          <p className="text-sm">No signs found matching your search.</p>
        </div>
      )}
    </div>
  );
};
