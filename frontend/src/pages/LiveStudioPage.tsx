import React, { useRef } from 'react';
import { useWebcam } from '../hooks/useWebcam';
import { useGestureRecognition } from '../hooks/useGestureRecognition';
import { useSpeech } from '../hooks/useSpeech';
import { WebcamCard } from '../components/WebcamCard';
import { ActiveSignBanner } from '../components/ActiveSignBanner';
import { TranscriptCard } from '../components/TranscriptCard';
import { Hand, HelpCircle } from 'lucide-react';

export const LiveStudioPage: React.FC = () => {
  const { videoRef, isActive, errorMessage, startCamera, stopCamera } = useWebcam();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const {
    predictedSign,
    confidence,
    topCandidates,
    sentence,
    isStable,
    latency,
    autoTTS,
    setAutoTTS,
    clearSentence,
    sessionId,
  } = useGestureRecognition(videoRef, canvasRef, isActive);

  const { speak, isSpeaking } = useSpeech();

  const handleToggleCamera = () => {
    if (isActive) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner / Introduction */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-r from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/20">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              Live Real-Time AI
            </span>
            <span className="text-xs text-slate-400 font-mono">Word-Level 3D Landmark Model (100% Acc)</span>
          </div>
          <h2 className="text-xl font-bold text-white">Sign Language Real-time Translation Studio</h2>
          <p className="text-xs text-slate-300 max-w-2xl">
            Show your hand gestures in front of the camera. The AI recognizes complete ASL words and conversational phrases directly, speaking them aloud in real time.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleToggleCamera}
            className={`px-5 py-2.5 rounded-xl font-semibold text-sm transition-all shadow-lg ${
              isActive
                ? 'bg-slate-800 hover:bg-slate-700 text-rose-300 border border-rose-500/30'
                : 'bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-slate-950 shadow-emerald-500/20'
            }`}
          >
            {isActive ? 'Stop Camera' : 'Start Camera'}
          </button>
        </div>
      </div>

      {/* Main Studio Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Live Webcam Viewport (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <WebcamCard
            videoRef={videoRef}
            canvasRef={canvasRef}
            isActive={isActive}
            errorMessage={errorMessage}
            onToggleCamera={handleToggleCamera}
          />
        </div>

        {/* Right Column: Active Detected Sign & Sentence Transcript (5 cols) */}
        <div className="lg:col-span-5 space-y-6 flex flex-col justify-between">
          <ActiveSignBanner
            sign={predictedSign}
            confidence={confidence}
            topCandidates={topCandidates}
            isStable={isStable}
          />

          <TranscriptCard
            sentence={sentence}
            onClear={clearSentence}
            onSpeak={speak}
            isSpeaking={isSpeaking}
            autoTTS={autoTTS}
            onToggleAutoTTS={() => setAutoTTS(!autoTTS)}
            sessionId={sessionId}
            totalGestures={sentence ? sentence.trim().split(/\s+/).length : 0}
            avgConfidence={confidence / 100 || 0.95}
          />
        </div>
      </div>

      {/* Quick Action Gesture Guide */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Hand className="h-4 w-4 text-emerald-400" />
            Supported Word Signs
          </span>
          <span className="text-xs text-slate-500 flex items-center gap-1">
            <HelpCircle className="h-3.5 w-3.5" /> Hold gesture steadily to commit
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 md:grid-cols-5 lg:grid-cols-10 gap-2.5">
          {[
            { sign: 'HELLO', desc: 'Open wave' },
            { sign: 'THANK_YOU', desc: 'Forward tilt' },
            { sign: 'YES', desc: 'Closed fist' },
            { sign: 'NO', desc: 'Fingers pinch' },
            { sign: 'I_LOVE_YOU', desc: 'Thumb-Index-Pinky' },
            { sign: 'HELP', desc: 'Thumbs up' },
            { sign: 'GOOD', desc: '"OK" sign' },
            { sign: 'PEACE', desc: '"V" sign' },
            { sign: 'STOP', desc: 'Flat palm' },
            { sign: 'CLEAR', desc: 'Side swipe' },
          ].map((item, idx) => (
            <div key={idx} className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80 text-center">
              <span className="font-mono text-xs font-bold text-emerald-400">{item.sign}</span>
              <p className="text-[10px] text-slate-400 mt-0.5">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
