import React, { useState } from 'react';
import { Volume2, Trash2, Copy, Check, BookmarkPlus, Sparkles } from 'lucide-react';
import { apiService } from '../services/api';

interface TranscriptCardProps {
  sentence: string;
  onClear: () => void;
  onSpeak: (text: string) => void;
  isSpeaking: boolean;
  autoTTS: boolean;
  onToggleAutoTTS: () => void;
  sessionId: string;
  totalGestures?: number;
  avgConfidence?: number;
}

export const TranscriptCard: React.FC<TranscriptCardProps> = ({
  sentence,
  onClear,
  onSpeak,
  isSpeaking,
  autoTTS,
  onToggleAutoTTS,
  sessionId,
  totalGestures = 1,
  avgConfidence = 0.95,
}) => {
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleCopy = () => {
    if (!sentence) return;
    navigator.clipboard.writeText(sentence);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSave = async () => {
    if (!sentence.trim()) return;
    try {
      await apiService.saveSession({
        session_id: sessionId,
        translated_text: sentence,
        total_gestures: totalGestures,
        avg_confidence: avgConfidence,
        duration_seconds: 30.0,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    } catch (err) {
      console.error('Failed to save session:', err);
    }
  };

  const wordCount = sentence.trim() ? sentence.trim().split(/\s+/).length : 0;
  const charCount = sentence.length;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Sparkles className="h-4 w-4 text-emerald-400" />
          <h2 className="text-sm font-semibold text-slate-200">Translated English Sentence</h2>
        </div>

        {/* Auto TTS toggle */}
        <label className="flex items-center space-x-2 text-xs text-slate-400 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={autoTTS}
            onChange={onToggleAutoTTS}
            className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-emerald-400 focus:ring-offset-slate-900"
          />
          <span>Auto Voice</span>
        </label>
      </div>

      {/* Transcript Text Display Box */}
      <div className="min-h-[110px] max-h-[180px] overflow-y-auto p-4 rounded-xl bg-slate-950/70 border border-slate-800/80 font-medium text-lg leading-relaxed text-slate-100 flex items-center">
        {sentence ? (
          <p className="w-full break-words">
            {sentence}
            <span className="inline-block w-2 h-5 ml-1 bg-emerald-400 animate-pulse align-middle" />
          </p>
        ) : (
          <p className="text-slate-500 text-sm italic">
            Perform sign gestures in front of the camera. Recognized letters and phrases will assemble into words and sentences here...
          </p>
        )}
      </div>

      {/* Metrics & Action Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
        <div className="flex items-center space-x-3 text-xs text-slate-400">
          <span>Words: <strong className="text-slate-200">{wordCount}</strong></span>
          <span>Chars: <strong className="text-slate-200">{charCount}</strong></span>
        </div>

        <div className="flex items-center space-x-2">
          {/* Speak Button */}
          <button
            onClick={() => onSpeak(sentence)}
            disabled={!sentence || isSpeaking}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <Volume2 className="h-3.5 w-3.5" />
            <span>{isSpeaking ? 'Speaking...' : 'Speak'}</span>
          </button>

          {/* Copy Button */}
          <button
            onClick={handleCopy}
            disabled={!sentence}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          {/* Save Session Button */}
          <button
            onClick={handleSave}
            disabled={!sentence.trim() || saved}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 text-xs font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            {saved ? <Check className="h-3.5 w-3.5 text-cyan-400" /> : <BookmarkPlus className="h-3.5 w-3.5" />}
            <span>{saved ? 'Saved' : 'Save'}</span>
          </button>

          {/* Clear Button */}
          <button
            onClick={onClear}
            disabled={!sentence}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-rose-400 text-xs font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
          >
            <Trash2 className="h-3.5 w-3.5" />
            <span>Clear</span>
          </button>
        </div>
      </div>
    </div>
  );
};
