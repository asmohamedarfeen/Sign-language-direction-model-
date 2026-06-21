/**
 * Utility for rendering 21-point MediaPipe hand skeleton landmarks on HTML5 Canvas.
 */

import { Landmark } from '../services/api';

const SKELETON_CONNECTIONS: [number, number][] = [
  // Palm base
  [0, 1], [0, 5], [0, 17], [5, 9], [9, 13], [13, 17],
  // Thumb
  [1, 2], [2, 3], [3, 4],
  // Index finger
  [5, 6], [6, 7], [7, 8],
  // Middle finger
  [9, 10], [10, 11], [11, 12],
  // Ring finger
  [13, 14], [14, 15], [15, 16],
  // Pinky finger
  [17, 18], [18, 19], [19, 20],
];

export function drawHandLandmarks(
  ctx: CanvasRenderingContext2D,
  landmarks: Landmark[],
  canvasWidth: number,
  canvasHeight: number,
  isMirrored: boolean = true
): void {
  ctx.save();

  // Clear previous frame
  ctx.clearRect(0, 0, canvasWidth, canvasHeight);

  // If mirrored, flip horizontally for natural mirror feel
  if (isMirrored) {
    ctx.translate(canvasWidth, 0);
    ctx.scale(-1, 1);
  }

  // 1. Draw Skeleton Connection Bones
  ctx.lineWidth = 3.5;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.strokeStyle = 'rgba(16, 185, 129, 0.85)'; // Neon Emerald glow

  for (const [startIdx, endIdx] of SKELETON_CONNECTIONS) {
    const p1 = landmarks[startIdx];
    const p2 = landmarks[endIdx];
    if (!p1 || !p2) continue;

    const x1 = p1.x * canvasWidth;
    const y1 = p1.y * canvasHeight;
    const x2 = p2.x * canvasWidth;
    const y2 = p2.y * canvasHeight;

    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  // 2. Draw Landmark Joints
  for (let i = 0; i < landmarks.length; i++) {
    const pt = landmarks[i];
    const x = pt.x * canvasWidth;
    const y = pt.y * canvasHeight;

    ctx.beginPath();
    // Fingertips (4, 8, 12, 16, 20) in bright cyan, joints in emerald
    const isFingertip = [4, 8, 12, 16, 20].includes(i);
    const radius = isFingertip ? 6.5 : 4.5;

    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fillStyle = isFingertip ? '#06b6d4' : '#10b981';
    ctx.fill();

    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#ffffff';
    ctx.stroke();
  }

  ctx.restore();
}
