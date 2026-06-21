import React from 'react';
import { Sparkles, CheckCircle2 } from 'lucide-react';
import { GestureCandidate } from '../services/api';

interface ActiveSignBannerProps {
  sign: string;
  confidence: number;
  topCandidates: GestureCandidate[];
  isStable: boolean;
}

export const ActiveSignBanner: React.FC<ActiveSignBannerProps> = ({
  sign,
  confidence,
  topCandidates,
  isStable,
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold flex items-center gap-1.5">
            <Sparkles className="h-3.5 w-3.5 text-cyan-400" />
            Detected Sign
          </span>
          {isStable && (
            <span className="inline-flex items-center gap-1 text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <CheckCircle2 className="h-3 w-3" />
              Locked & Committed
            </span>
          )}
        </div>

        {/* Large Gesture Representation */}
        <div className="flex items-baseline space-x-4 my-2">
          <div className="text-6xl font-black tracking-tight text-white font-mono bg-gradient-to-br from-emerald-300 via-teal-200 to-cyan-300 bg-clip-text text-transparent">
            {sign !== '---' ? sign : 'Waiting...'}
          </div>
          {confidence > 0 && (
            <div className="text-sm font-semibold text-emerald-400 bg-emerald-950/60 border border-emerald-800/40 px-2.5 py-1 rounded-lg">
              {confidence.toFixed(1)}% Match
            </div>
          )}
        </div>
      </div>

      {/* Probability Distribution */}
      {topCandidates && topCandidates.length > 0 && (
        <div className="mt-4 pt-4 border-t border-slate-800/80">
          <p className="text-xs text-slate-400 mb-2 font-medium">Confidence Breakdown:</p>
          <div className="space-y-2">
            {topCandidates.slice(0, 3).map((candidate, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-xs text-slate-300">
                  <span className="font-mono font-medium">{candidate.label}</span>
                  <span className="text-slate-400">{candidate.percentage}%</span>
                </div>
                <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-200 ${
                      idx === 0 ? 'bg-gradient-to-r from-emerald-500 to-cyan-400' : 'bg-slate-600'
                    }`}
                    style={{ width: `${Math.min(100, Math.max(0, candidate.percentage))}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
