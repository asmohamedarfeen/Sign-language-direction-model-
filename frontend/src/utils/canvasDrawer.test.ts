import { describe, it, expect, vi } from 'vitest';
import { drawHandLandmarks } from './canvasDrawer';
import { Landmark } from '../services/api';

describe('canvasDrawer', () => {
  it('should clear canvas and draw skeleton bones and joints without error', () => {
    const mockCtx = {
      save: vi.fn(),
      restore: vi.fn(),
      clearRect: vi.fn(),
      translate: vi.fn(),
      scale: vi.fn(),
      beginPath: vi.fn(),
      moveTo: vi.fn(),
      lineTo: vi.fn(),
      stroke: vi.fn(),
      arc: vi.fn(),
      fill: vi.fn(),
      lineWidth: 0,
      lineCap: '',
      lineJoin: '',
      strokeStyle: '',
      fillStyle: '',
    } as unknown as CanvasRenderingContext2D;

    const mockLandmarks: Landmark[] = Array.from({ length: 21 }, (_, i) => ({
      x: 0.1 * (i % 5),
      y: 0.1 * Math.floor(i / 5),
      z: 0.0,
    }));

    drawHandLandmarks(mockCtx, mockLandmarks, 640, 480, true);

    expect(mockCtx.save).toHaveBeenCalled();
    expect(mockCtx.clearRect).toHaveBeenCalledWith(0, 0, 640, 480);
    expect(mockCtx.translate).toHaveBeenCalledWith(640, 0);
    expect(mockCtx.scale).toHaveBeenCalledWith(-1, 1);
    expect(mockCtx.stroke).toHaveBeenCalled();
    expect(mockCtx.fill).toHaveBeenCalled();
    expect(mockCtx.restore).toHaveBeenCalled();
  });
});
