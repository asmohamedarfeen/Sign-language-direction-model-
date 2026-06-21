/**
 * API Service for Sign Language Translation Backend.
 * Encapsulates all HTTP and WebSocket network calls.
 */

const BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export interface Landmark {
  x: number;
  y: number;
  z?: number;
}

export interface GestureCandidate {
  label: string;
  confidence: number;
  percentage: number;
}

export interface GesturePredictResponse {
  predicted_sign: string;
  confidence: number;
  percentage: number;
  top_candidates: GestureCandidate[];
  current_sentence: string;
  latency_ms: number;
  is_stable: boolean;
}

export interface SignItem {
  id: number;
  symbol: string;
  label: string;
  category: string;
  description?: string;
  tips?: string;
  image_url?: string;
}

export interface TranslationSession {
  id: number;
  session_id: string;
  translated_text: string;
  total_gestures: number;
  avg_confidence: number;
  duration_seconds: number;
  created_at: string;
}

export interface AnalyticsSummary {
  total_sessions: number;
  total_words_translated: number;
  overall_avg_confidence: number;
  total_gestures_processed: number;
}

export const apiService = {
  /** Single frame inference */
  async predictGesture(
    landmarks: Landmark[],
    handedness: string = 'Right',
    sessionId: string = 'web_session'
  ): Promise<GesturePredictResponse> {
    const res = await fetch(`${BASE_URL}/recognition/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        landmarks,
        handedness,
        session_id: sessionId,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.message || 'Failed to predict gesture');
    }
    return res.json();
  },

  /** Reset sentence buffer */
  async resetSentence(sessionId: string = 'web_session'): Promise<{ current_sentence: string }> {
    const res = await fetch(`${BASE_URL}/recognition/reset`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId }),
    });
    return res.json();
  },

  /** Fetch sign vocabulary */
  async getVocabulary(category?: string): Promise<SignItem[]> {
    const url = category
      ? `${BASE_URL}/vocabulary?category=${encodeURIComponent(category)}`
      : `${BASE_URL}/vocabulary`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch vocabulary');
    return res.json();
  },

  /** Fetch translation history */
  async getHistory(limit: number = 50, offset: number = 0): Promise<TranslationSession[]> {
    const res = await fetch(`${BASE_URL}/history?limit=${limit}&offset=${offset}`);
    if (!res.ok) throw new Error('Failed to fetch translation history');
    return res.json();
  },

  /** Save a session record */
  async saveSession(payload: {
    session_id: string;
    translated_text: string;
    total_gestures: number;
    avg_confidence: number;
    duration_seconds: number;
  }): Promise<TranslationSession> {
    const res = await fetch(`${BASE_URL}/history`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to save session');
    return res.json();
  },

  /** Delete a session record */
  async deleteSession(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/history/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete session');
  },

  /** Fetch summary stats */
  async getAnalytics(): Promise<AnalyticsSummary> {
    const res = await fetch(`${BASE_URL}/history/analytics/summary`);
    if (!res.ok) throw new Error('Failed to fetch analytics');
    return res.json();
  },
};
