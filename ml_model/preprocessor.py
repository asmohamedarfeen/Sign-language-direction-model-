"""
Sign Language Landmark Preprocessor.

Extracts scale-, translation-, and handedness-invariant features
from 21 3D MediaPipe hand landmarks.
"""

from typing import List, Dict, Union, Any
import numpy as np


# Joint indices according to MediaPipe Hands topology
WRIST = 0
THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4
INDEX_MCP = 5
INDEX_PIP = 6
INDEX_DIP = 7
INDEX_TIP = 8
MIDDLE_MCP = 9
MIDDLE_PIP = 10
MIDDLE_DIP = 11
MIDDLE_TIP = 12
RING_MCP = 13
RING_PIP = 14
RING_DIP = 15
RING_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20

FINGERTIP_INDICES = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
MCP_INDICES = [THUMB_MCP, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP]


class LandmarkPreprocessor:
    """
    Normalizes 21 3D hand landmarks into a discriminative feature vector.
    """

    FEATURE_DIM: int = 83  # 63 normalized coordinates + 20 geometric features

    @classmethod
    def landmarks_to_array(
        cls,
        landmarks: Union[List[Dict[str, float]], List[List[float]], np.ndarray]
    ) -> np.ndarray:
        """
        Converts diverse input landmark formats into a (21, 3) float32 numpy array.
        """
        if isinstance(landmarks, np.ndarray):
            arr = landmarks.astype(np.float32)
            if arr.ndim == 1:
                arr = arr.reshape((21, 3))
            return arr

        if len(landmarks) == 0:
            raise ValueError("Landmarks list cannot be empty.")

        first = landmarks[0]
        if isinstance(first, dict):
            pts = []
            for p in landmarks:
                pts.append([
                    float(p.get("x", 0.0)),
                    float(p.get("y", 0.0)),
                    float(p.get("z", 0.0))
                ])
            return np.array(pts, dtype=np.float32)
        elif isinstance(first, (list, tuple)):
            return np.array(landmarks, dtype=np.float32)
        else:
            raise TypeError(f"Unsupported landmarks element type: {type(first)}")

    @classmethod
    def normalize_landmarks(
        cls,
        coords: np.ndarray,
        flip_horizontal: bool = False
    ) -> np.ndarray:
        """
        Normalizes (21, 3) coordinates:
        1. Translates wrist to (0, 0, 0)
        2. Optionally mirrors X if left hand to match canonical right-hand training set
        3. Scales coordinates so palm distance (wrist to middle MCP) is 1.0
        """
        norm_coords = coords.copy()

        # 1. Wrist translation
        wrist = norm_coords[WRIST, :].copy()
        norm_coords -= wrist

        # 2. Mirror if left hand
        if flip_horizontal:
            norm_coords[:, 0] = -norm_coords[:, 0]

        # 3. Scale normalization
        palm_dist = np.linalg.norm(norm_coords[MIDDLE_MCP])
        if palm_dist < 1e-6:
            # Fallback to index MCP if middle is degenerate
            palm_dist = np.linalg.norm(norm_coords[INDEX_MCP])
            if palm_dist < 1e-6:
                palm_dist = 1.0

        norm_coords /= palm_dist
        return norm_coords

    @classmethod
    def extract_features(
        cls,
        landmarks: Union[List[Dict[str, float]], List[List[float]], np.ndarray],
        handedness: str = "Right"
    ) -> np.ndarray:
        """
        Extracts the full 83-dimensional feature vector.
        
        Vector structure:
        - [0:63]   : 21 normalized 3D coordinates (x, y, z)
        - [63:68]  : Euclidean distances from wrist to each of 5 fingertips
        - [68:72]  : Adjacent fingertip distances (thumb-index, index-mid, mid-ring, ring-pinky)
        - [72:77]  : Finger curl metrics (distance from fingertip to its respective MCP joint)
        - [77:83]  : Key inter-finger direction cosines / angles
        """
        raw_coords = cls.landmarks_to_array(landmarks)
        if raw_coords.shape != (21, 3):
            raise ValueError(f"Expected shape (21, 3), got {raw_coords.shape}")

        is_left = (handedness.lower() == "left")
        norm_coords = cls.normalize_landmarks(raw_coords, flip_horizontal=is_left)

        # 1. Flattened coordinates (63)
        coord_features = norm_coords.flatten()

        # 2. Wrist to fingertip distances (5)
        wrist_tip_dists = [
            float(np.linalg.norm(norm_coords[tip])) for tip in FINGERTIP_INDICES
        ]

        # 3. Adjacent fingertip distances (4)
        adj_tip_dists = [
            float(np.linalg.norm(norm_coords[THUMB_TIP] - norm_coords[INDEX_TIP])),
            float(np.linalg.norm(norm_coords[INDEX_TIP] - norm_coords[MIDDLE_TIP])),
            float(np.linalg.norm(norm_coords[MIDDLE_TIP] - norm_coords[RING_TIP])),
            float(np.linalg.norm(norm_coords[RING_TIP] - norm_coords[PINKY_TIP])),
        ]

        # 4. Finger extension/curl distances (5)
        curl_dists = [
            float(np.linalg.norm(norm_coords[tip] - norm_coords[mcp]))
            for tip, mcp in zip(FINGERTIP_INDICES, MCP_INDICES)
        ]

        # 5. Inter-finger cosine angles (6)
        def cosine_angle(v1: np.ndarray, v2: np.ndarray) -> float:
            n1 = np.linalg.norm(v1)
            n2 = np.linalg.norm(v2)
            if n1 < 1e-6 or n2 < 1e-6:
                return 0.0
            return float(np.dot(v1, v2) / (n1 * n2))

        angles = [
            cosine_angle(norm_coords[INDEX_TIP] - norm_coords[INDEX_MCP],
                         norm_coords[MIDDLE_TIP] - norm_coords[MIDDLE_MCP]),
            cosine_angle(norm_coords[MIDDLE_TIP] - norm_coords[MIDDLE_MCP],
                         norm_coords[RING_TIP] - norm_coords[RING_MCP]),
            cosine_angle(norm_coords[RING_TIP] - norm_coords[RING_MCP],
                         norm_coords[PINKY_TIP] - norm_coords[PINKY_MCP]),
            cosine_angle(norm_coords[THUMB_TIP] - norm_coords[THUMB_MCP],
                         norm_coords[INDEX_TIP] - norm_coords[INDEX_MCP]),
            cosine_angle(norm_coords[INDEX_TIP], norm_coords[PINKY_TIP]),
            cosine_angle(norm_coords[THUMB_TIP], norm_coords[PINKY_TIP]),
        ]

        feature_vector = np.concatenate([
            coord_features,
            np.array(wrist_tip_dists, dtype=np.float32),
            np.array(adj_tip_dists, dtype=np.float32),
            np.array(curl_dists, dtype=np.float32),
            np.array(angles, dtype=np.float32),
        ]).astype(np.float32)

        return feature_vector
