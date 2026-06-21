import React, { useState, useEffect } from 'react';
import { apiService, TranslationSession, AnalyticsSummary } from '../services/api';
import { useSpeech } from '../hooks/useSpeech';
import { History, Volume2, Trash2, Calendar, Award, MessageSquare, Flame } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const [sessions, setSessions] = useState<TranslationSession[]>([]);
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const { speak, isSpeaking } = useSpeech();

  const loadData = async () => {
    try {
      setLoading(true);
      const [historyData, statsData] = await Promise.all([
        apiService.getHistory(),
        apiService.getAnalytics(),
      ]);
      setSessions(historyData);
      setAnalytics(statsData);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDelete = async (id: number) => {
    try {
      await apiService.deleteSession(id);
      setSessions(sessions.filter((s) => s.id !== id));
      // Refresh stats
      const stats = await apiService.getAnalytics();
      setAnalytics(stats);
    } catch (err) {
      console.error('Failed to delete session:', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800">
        <div className="flex items-center space-x-2 mb-1">
          <History className="h-5 w-5 text-emerald-400" />
          <h2 className="text-xl font-bold text-white">Translation History & Analytics</h2>
        </div>
        <p className="text-xs text-slate-400">
          Review past translated sentences, listen to audio playbacks, and track translation volume.
        </p>
      </div>

      {/* Analytics Stats Cards */}
      {analytics && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
            <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
              <MessageSquare className="h-4 w-4 text-emerald-400" />
              <span>Saved Sessions</span>
            </div>
            <div className="text-2xl font-black text-white">{analytics.total_sessions}</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
            <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
              <Flame className="h-4 w-4 text-cyan-400" />
              <span>Words Translated</span>
            </div>
            <div className="text-2xl font-black text-white">{analytics.total_words_translated}</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
            <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
              <Award className="h-4 w-4 text-teal-400" />
              <span>Avg Confidence</span>
            </div>
            <div className="text-2xl font-black text-white">
              {(analytics.overall_avg_confidence * 100).toFixed(1)}%
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
            <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
              <Calendar className="h-4 w-4 text-purple-400" />
              <span>Gestures Processed</span>
            </div>
            <div className="text-2xl font-black text-white">{analytics.total_gestures_processed}</div>
          </div>
        </div>
      )}

      {/* Sessions List */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <h3 className="text-sm font-bold text-slate-200 mb-4">Saved Translation Transcripts</h3>

        {loading && (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-20 rounded-xl bg-slate-950/60 border border-slate-800 animate-pulse" />
            ))}
          </div>
        )}

        {!loading && sessions.length === 0 && (
          <div className="text-center py-12 text-slate-500">
            <History className="h-8 w-8 mx-auto mb-2 opacity-40" />
            <p className="text-sm">No translation sessions saved yet.</p>
            <p className="text-xs text-slate-600 mt-1">Translate a sentence in the Live Studio and click 'Save'.</p>
          </div>
        )}

        {!loading && sessions.length > 0 && (
          <div className="space-y-3">
            {sessions.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 transition-all"
              >
                <div className="space-y-1">
                  <p className="font-semibold text-base text-slate-100">{item.translated_text}</p>
                  <div className="flex items-center space-x-3 text-xs text-slate-400">
                    <span>{new Date(item.created_at).toLocaleString()}</span>
                    <span>•</span>
                    <span>Gestures: <strong className="text-slate-300">{item.total_gestures}</strong></span>
                    <span>•</span>
                    <span>Accuracy: <strong className="text-emerald-400">{(item.avg_confidence * 100).toFixed(0)}%</strong></span>
                  </div>
                </div>

                <div className="flex items-center space-x-2 shrink-0">
                  <button
                    onClick={() => speak(item.translated_text)}
                    disabled={isSpeaking}
                    className="p-2 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/20 text-xs font-semibold"
                    title="Speak text"
                  >
                    <Volume2 className="h-4 w-4" />
                  </button>

                  <button
                    onClick={() => handleDelete(item.id)}
                    className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-rose-400 border border-rose-500/10 text-xs font-semibold"
                    title="Delete record"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
