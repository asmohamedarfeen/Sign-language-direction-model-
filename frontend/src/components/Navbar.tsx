import React from 'react';
import { HandMetal, BookOpen, History, Video, Activity } from 'lucide-react';

interface NavbarProps {
  currentTab: 'studio' | 'dictionary' | 'history';
  onSelectTab: (tab: 'studio' | 'dictionary' | 'history') => void;
  latencyMs?: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  onSelectTab,
  latencyMs = 0,
}) => {
  return (
    <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => onSelectTab('studio')}>
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-400 to-cyan-500 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <HandMetal className="h-6 w-6 text-slate-950 font-bold" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
              SignSpeak
            </h1>
            <p className="text-xs text-slate-400">Sign Language to English AI</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center space-x-1 sm:space-x-2">
          <button
            onClick={() => onSelectTab('studio')}
            className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
              currentTab === 'studio'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <Video className="h-4 w-4" />
            <span>Live Studio</span>
          </button>

          <button
            onClick={() => onSelectTab('dictionary')}
            className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
              currentTab === 'dictionary'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <BookOpen className="h-4 w-4" />
            <span>Dictionary</span>
          </button>

          <button
            onClick={() => onSelectTab('history')}
            className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ${
              currentTab === 'history'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <History className="h-4 w-4" />
            <span>History</span>
          </button>
        </nav>

        {/* Status Indicator */}
        <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs">
          <Activity className="h-3.5 w-3.5 text-emerald-400 animate-pulse" />
          <span className="text-slate-300">Latency:</span>
          <span className="font-mono text-emerald-400">{latencyMs > 0 ? `${latencyMs}ms` : '< 20ms'}</span>
        </div>
      </div>
    </header>
  );
};
