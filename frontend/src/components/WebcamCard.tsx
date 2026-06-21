import React from 'react';
import { Camera, CameraOff, AlertCircle } from 'lucide-react';

interface WebcamCardProps {
  videoRef: React.RefObject<HTMLVideoElement>;
  canvasRef: React.RefObject<HTMLCanvasElement>;
  isActive: boolean;
  errorMessage: string | null;
  onToggleCamera: () => void;
}

export const WebcamCard: React.FC<WebcamCardProps> = ({
  videoRef,
  canvasRef,
  isActive,
  errorMessage,
  onToggleCamera,
}) => {
  return (
    <div className="relative bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col">
      {/* Video / Canvas Viewport */}
      <div className="relative aspect-video w-full bg-slate-950 flex items-center justify-center overflow-hidden">
        {/* Hidden video stream element used by MediaPipe */}
        <video
          ref={videoRef}
          playsInline
          muted
          autoPlay
          className={`w-full h-full object-cover transform -scale-x-100 ${
            isActive ? 'block' : 'hidden'
          }`}
        />

        {/* Transparent Canvas overlay for joint skeleton rendering */}
        <canvas
          ref={canvasRef}
          width={640}
          height={480}
          className={`absolute inset-0 w-full h-full object-cover pointer-events-none ${
            isActive ? 'block' : 'hidden'
          }`}
        />

        {/* Inactive State Screen */}
        {!isActive && !errorMessage && (
          <div className="text-center p-6 space-y-3">
            <div className="h-14 w-14 mx-auto rounded-2xl bg-slate-800/80 flex items-center justify-center text-slate-400">
              <Camera className="h-7 w-7" />
            </div>
            <div>
              <h3 className="text-base font-semibold text-slate-200">Camera is off</h3>
              <p className="text-xs text-slate-400 max-w-xs mt-1">
                Start your camera to enable real-time 3D hand tracking and sign translation.
              </p>
            </div>
            <button
              onClick={onToggleCamera}
              className="mt-2 inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 font-semibold text-slate-950 text-sm shadow-lg shadow-emerald-500/20 transition-all"
            >
              <Camera className="h-4 w-4" />
              <span>Enable Camera</span>
            </button>
          </div>
        )}

        {/* Error Screen */}
        {errorMessage && (
          <div className="text-center p-6 space-y-3 text-rose-400">
            <AlertCircle className="h-10 w-10 mx-auto text-rose-400" />
            <p className="text-sm font-medium">{errorMessage}</p>
            <button
              onClick={onToggleCamera}
              className="px-4 py-2 rounded-lg bg-rose-500/20 border border-rose-500/30 text-rose-300 text-xs font-semibold hover:bg-rose-500/30"
            >
              Retry
            </button>
          </div>
        )}

        {/* Live Tracking Status Pill */}
        {isActive && (
          <div className="absolute top-3 left-3 flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-900/80 backdrop-blur-md border border-slate-700/60 text-xs">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-slate-200 font-medium">Tracking Hands</span>
          </div>
        )}
      </div>

      {/* Camera Toolbar */}
      <div className="p-3.5 bg-slate-900 border-t border-slate-800 flex items-center justify-between">
        <span className="text-xs text-slate-400">
          {isActive ? 'Camera running at 640×480' : 'Standby'}
        </span>
        {isActive && (
          <button
            onClick={onToggleCamera}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-rose-300 border border-rose-500/20 transition-colors"
          >
            <CameraOff className="h-3.5 w-3.5" />
            <span>Turn Off</span>
          </button>
        )}
      </div>
    </div>
  );
};
