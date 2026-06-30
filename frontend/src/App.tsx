import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { LiveStudioPage } from './pages/LiveStudioPage';
import { VocabularyPage } from './pages/VocabularyPage';
import { HistoryPage } from './pages/HistoryPage';

export const App: React.FC = () => {
  const urlTab = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('tab') : null;
  const initialTab = (urlTab === 'dictionary' || urlTab === 'history') ? urlTab : 'studio';
  const [currentTab, setCurrentTab] = useState<'studio' | 'dictionary' | 'history'>(initialTab);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar currentTab={currentTab} onSelectTab={setCurrentTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {currentTab === 'studio' && <LiveStudioPage />}
        {currentTab === 'dictionary' && <VocabularyPage />}
        {currentTab === 'history' && <HistoryPage />}
      </main>

      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <p>SignSpeak — Real-Time Sign Language to English Translation AI System</p>
      </footer>
    </div>
  );
};

export default App;
