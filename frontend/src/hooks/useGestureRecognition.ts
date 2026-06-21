import { useState, useRef, useCallback, useEffect } from 'react';
import { apiService, GesturePredictResponse, GestureCandidate, Landmark } from '../services/api';
import { drawHandLandmarks } from '../utils/canvasDrawer';
import { useSpeech } from './useSpeech';

declare global {
  interface Window {
    Hands?: any;
    Camera?: any;
  }
}

export function useGestureRecognition(
  videoRef: React.RefObject<HTMLVideoElement>,
  canvasRef: React.RefObject<HTMLCanvasElement>,
  isCameraActive: boolean
) {
  const [predictedSign, setPredictedSign] = useState<string>('---');
  const [confidence, setConfidence] = useState<number>(0);
  const [topCandidates, setTopCandidates] = useState<GestureCandidate[]>([]);
  const [sentence, setSentence] = useState<string>('');
  const [isStable, setIsStable] = useState<boolean>(false);
  const [latency, setLatency] = useState<number>(0);
  const [autoTTS, setAutoTTS] = useState<boolean>(true);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const { speak } = useSpeech();
  const handsInstanceRef = useRef<any>(null);
  const lastProcessedTimeRef = useRef<number>(0);
  const sessionIdRef = useRef<string>(`session_${Date.now()}`);
  const previousSentenceRef = useRef<string>('');

  // Handle incoming MediaPipe hand tracking results
  const onResults = useCallback(async (results: any) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    if (!results.multiHandLandmarks || results.multiHandLandmarks.length === 0) {
      // Clear canvas if no hands visible
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      return;
    }

    const firstHandLandmarks: Landmark[] = results.multiHandLandmarks[0];
    const handedness = results.multiHandedness?.[0]?.label || 'Right';

    // Draw visual skeleton overlay
    drawHandLandmarks(ctx, firstHandLandmarks, canvas.width, canvas.height, true);

    // Throttle inference requests to ~10-15 FPS (every 70ms) to avoid network congestion
    const now = performance.now();
    if (now - lastProcessedTimeRef.current < 70 || isProcessing) {
      return;
    }
    lastProcessedTimeRef.current = now;

    try {
      setIsProcessing(true);
      const res: GesturePredictResponse = await apiService.predictGesture(
        firstHandLandmarks,
        handedness,
        sessionIdRef.current
      );

      setPredictedSign(res.predicted_sign);
      setConfidence(res.percentage);
      setTopCandidates(res.top_candidates);
      setSentence(res.current_sentence);
      setIsStable(res.is_stable);
      setLatency(res.latency_ms);

      // Auto-speak new word if sentence ended with space or changed significantly
      if (autoTTS && res.current_sentence !== previousSentenceRef.current) {
        const prev = previousSentenceRef.current;
        const curr = res.current_sentence;
        if (curr.length > prev.length && (curr.endsWith(' ') || curr.length - prev.length > 2)) {
          const newPart = curr.slice(prev.length).trim();
          if (newPart) {
            speak(newPart);
          }
        }
        previousSentenceRef.current = curr;
      }
    } catch (err) {
      console.warn('Inference request failed:', err);
    } finally {
      setIsProcessing(false);
    }
  }, [canvasRef, autoTTS, isProcessing, speak]);

  // Initialize MediaPipe Hands detector
  useEffect(() => {
    if (!isCameraActive || !videoRef.current) return;

    let animFrameId: number;
    let hands: any = null;

    if (window.Hands) {
      hands = new window.Hands({
        locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
      });

      hands.setOptions({
        maxNumHands: 1,
        modelComplexity: 1,
        minDetectionConfidence: 0.65,
        minTrackingConfidence: 0.65,
      });

      hands.onResults(onResults);
      handsInstanceRef.current = hands;

      const sendFrame = async () => {
        if (videoRef.current && videoRef.current.readyState >= 2) {
          await hands.send({ image: videoRef.current });
        }
        animFrameId = requestAnimationFrame(sendFrame);
      };

      animFrameId = requestAnimationFrame(sendFrame);
    }

    return () => {
      if (animFrameId) cancelAnimationFrame(animFrameId);
      if (hands) hands.close();
    };
  }, [isCameraActive, videoRef, onResults]);

  // Clear current transcript
  const clearSentence = useCallback(async () => {
    try {
      await apiService.resetSentence(sessionIdRef.current);
      setSentence('');
      previousSentenceRef.current = '';
    } catch (err) {
      console.error('Failed to reset sentence:', err);
    }
  }, []);

  return {
    predictedSign,
    confidence,
    topCandidates,
    sentence,
    isStable,
    latency,
    autoTTS,
    setAutoTTS,
    clearSentence,
    sessionId: sessionIdRef.current,
  };
}
