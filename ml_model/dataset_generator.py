"""
Dataset Generator & Biological Hand Landmark Synthesizer.

Defines canonical hand joint templates for conversational ASL words and controls,
applies 3D biomechanical rotations, joint jittering, scaling, and finger flex variations
to generate a high-accuracy landmark dataset matching MediaPipe camera coordinates.
"""

import os
from typing import Dict, List, Tuple
import numpy as np
from ml_model.preprocessor import (
    LandmarkPreprocessor,
    WRIST, THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP,
    INDEX_MCP, INDEX_PIP, INDEX_DIP, INDEX_TIP,
    MIDDLE_MCP, MIDDLE_PIP, MIDDLE_DIP, MIDDLE_TIP,
    RING_MCP, RING_PIP, RING_DIP, RING_TIP,
    PINKY_MCP, PINKY_PIP, PINKY_DIP, PINKY_TIP,
)


def get_base_neutral_hand() -> np.ndarray:
    """
    Returns base anatomical 21 (x, y, z) coordinates for an open upright hand.
    Wrist is at (0, 0, 0).
    Upward fingers have negative Y matching MediaPipe camera coordinates (y=0 top of frame).
    """
    hand = np.zeros((21, 3), dtype=np.float32)

    # Wrist
    hand[WRIST] = [0.0, 0.0, 0.0]

    # Thumb (abducted to left, slightly forward)
    hand[THUMB_CMC] = [-0.35, -0.25, -0.05]
    hand[THUMB_MCP] = [-0.60, -0.50, -0.08]
    hand[THUMB_IP]  = [-0.75, -0.75, -0.06]
    hand[THUMB_TIP] = [-0.85, -0.95, -0.04]

    # Index finger
    hand[INDEX_MCP] = [-0.30, -0.95, -0.02]
    hand[INDEX_PIP] = [-0.35, -1.35, -0.01]
    hand[INDEX_DIP] = [-0.38, -1.65, -0.01]
    hand[INDEX_TIP] = [-0.40, -1.95,  0.00]

    # Middle finger
    hand[MIDDLE_MCP] = [0.00, -1.00,  0.00]
    hand[MIDDLE_PIP] = [0.00, -1.45,  0.00]
    hand[MIDDLE_DIP] = [0.00, -1.80,  0.00]
    hand[MIDDLE_TIP] = [0.00, -2.10,  0.00]

    # Ring finger
    hand[RING_MCP] = [0.28, -0.92, -0.02]
    hand[RING_PIP] = [0.33, -1.32, -0.01]
    hand[RING_DIP] = [0.36, -1.62, -0.01]
    hand[RING_TIP] = [0.38, -1.90,  0.00]

    # Pinky finger
    hand[PINKY_MCP] = [0.52, -0.80, -0.04]
    hand[PINKY_PIP] = [0.62, -1.15, -0.03]
    hand[PINKY_DIP] = [0.68, -1.40, -0.02]
    hand[PINKY_TIP] = [0.72, -1.65, -0.01]

    return hand


def curl_finger(
    hand: np.ndarray,
    finger: str,
    curl_factor: float = 1.0
) -> None:
    """
    Simulates natural human finger curling towards the palm (0.0=straight, 1.0=fully curled fist).
    Curling brings fingertips closer to their respective MCP joint and arches forward in Z.
    """
    f_map = {
        "thumb":  (THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP),
        "index":  (INDEX_MCP, INDEX_PIP, INDEX_DIP, INDEX_TIP),
        "middle": (MIDDLE_MCP, MIDDLE_PIP, MIDDLE_DIP, MIDDLE_TIP),
        "ring":   (RING_MCP, RING_PIP, RING_DIP, RING_TIP),
        "pinky":  (PINKY_MCP, PINKY_PIP, PINKY_DIP, PINKY_TIP),
    }
    mcp, pip, dip, tip = f_map[finger]

    if finger == "thumb":
        target_tip = hand[INDEX_MCP] + np.array([0.15, 0.20, 0.25], dtype=np.float32)
        hand[tip] = hand[tip] * (1 - curl_factor) + target_tip * curl_factor
        hand[dip] = hand[dip] * (1 - curl_factor) + (target_tip * 0.85 + hand[mcp] * 0.15) * curl_factor
    else:
        mcp_pos = hand[mcp]
        hand[pip] = mcp_pos + (hand[pip] - mcp_pos) * (1.0 - 0.4 * curl_factor) + np.array([0, 0.20 * curl_factor, 0.25 * curl_factor])
        hand[dip] = mcp_pos + np.array([0, 0.10 * curl_factor, 0.45 * curl_factor])
        hand[tip] = mcp_pos + np.array([0, 0.25 * curl_factor, 0.30 * curl_factor])


def spread_fingers(hand: np.ndarray, factor: float = 1.0) -> None:
    """Spreads or closes fingers horizontally."""
    for idx in [INDEX_MCP, INDEX_PIP, INDEX_DIP, INDEX_TIP]:
        hand[idx, 0] *= factor
    for idx in [RING_MCP, RING_PIP, RING_DIP, RING_TIP]:
        hand[idx, 0] *= factor
    for idx in [PINKY_MCP, PINKY_PIP, PINKY_DIP, PINKY_TIP]:
        hand[idx, 0] *= factor


def define_canonical_gestures() -> Dict[str, np.ndarray]:
    """
    Constructs high-precision anatomically verified 3D landmark templates
    for complete ASL words and key conversational signs.
    """
    gestures: Dict[str, np.ndarray] = {}

    # 1. HELLO: Upright open flat hand facing camera (waving pose), all fingers extended
    h_hello = get_base_neutral_hand()
    spread_fingers(h_hello, 1.15)
    gestures["HELLO"] = h_hello

    # 2. THANK_YOU: Flat hand moving forward/tilted toward the camera from chin
    # Pronounced forward tilt (Z depth) and fingers kept close together
    h_thanks = get_base_neutral_hand()
    spread_fingers(h_thanks, 0.70)
    for idx in range(1, 21):
        frac = abs(h_thanks[idx, 1]) / 2.1  # distance along finger
        h_thanks[idx, 2] += frac * 0.85      # forward projection in Z
        h_thanks[idx, 1] *= 0.75             # foreshortened in Y due to forward tilt
    gestures["THANK_YOU"] = h_thanks

    # 3. YES: Closed fist representing head nod, thumb wrapped across front
    h_yes = get_base_neutral_hand()
    for f in ["index", "middle", "ring", "pinky", "thumb"]:
        curl_finger(h_yes, f, 1.0)
    h_yes[THUMB_TIP] = np.array([0.1, -0.8, 0.35])
    gestures["YES"] = h_yes

    # 4. NO: Index and middle fingers extended together pinching against thumb tip; ring/pinky curled
    h_no = get_base_neutral_hand()
    curl_finger(h_no, "ring", 1.0)
    curl_finger(h_no, "pinky", 1.0)
    snap_pos = np.array([-0.15, -1.25, 0.25])
    h_no[INDEX_TIP]  = snap_pos
    h_no[MIDDLE_TIP] = snap_pos + np.array([0.05, 0.0, 0.0])
    h_no[THUMB_TIP]  = snap_pos + np.array([-0.05, 0.0, 0.0])
    gestures["NO"] = h_no

    # 5. I_LOVE_YOU: ASL ILY sign (Thumb, Index, and Pinky extended, Middle and Ring curled)
    h_ily = get_base_neutral_hand()
    curl_finger(h_ily, "middle", 1.0)
    curl_finger(h_ily, "ring", 1.0)
    h_ily[THUMB_TIP] = np.array([-1.1, -0.7, 0.0])
    h_ily[PINKY_TIP] = np.array([0.80, -1.65, 0.0])
    gestures["I_LOVE_YOU"] = h_ily

    # 6. HELP: Thumbs-up gesture (Thumb extended upward, all other 4 fingers curled)
    h_help = get_base_neutral_hand()
    for f in ["index", "middle", "ring", "pinky"]:
        curl_finger(h_help, f, 1.0)
    h_help[THUMB_CMC] = [-0.15, -0.30, 0.05]
    h_help[THUMB_MCP] = [-0.20, -0.70, 0.08]
    h_help[THUMB_IP]  = [-0.20, -1.20, 0.10]
    h_help[THUMB_TIP] = [-0.20, -1.65, 0.12]
    gestures["HELP"] = h_help

    # 7. GOOD: "OK" sign (Thumb and index form a circle, middle/ring/pinky extended upright)
    h_good = get_base_neutral_hand()
    ok_pt = np.array([-0.25, -1.30, 0.15])
    h_good[INDEX_TIP] = ok_pt
    h_good[THUMB_TIP] = ok_pt
    spread_fingers(h_good, 1.2)
    gestures["GOOD"] = h_good

    # 8. PEACE: Victory "V" sign (Index and Middle extended in V, Ring, Pinky, and Thumb curled)
    h_peace = get_base_neutral_hand()
    curl_finger(h_peace, "ring", 1.0)
    curl_finger(h_peace, "pinky", 1.0)
    curl_finger(h_peace, "thumb", 1.0)
    h_peace[INDEX_TIP]  = np.array([-0.45, -1.95, 0.0])
    h_peace[MIDDLE_TIP] = np.array([0.35, -1.95, 0.0])
    gestures["PEACE"] = h_peace

    # 9. STOP: Open flat hand held forward with fingers pressed tightly together, thumb tucked
    h_stop = get_base_neutral_hand()
    spread_fingers(h_stop, 0.55)
    h_stop[THUMB_TIP] = np.array([-0.45, -0.90, 0.05])
    gestures["STOP"] = h_stop

    # 10. CLEAR: Control action - flat hand angled horizontally sideways (wipe gesture)
    h_clear = get_base_neutral_hand()
    rot_angle = np.radians(85.0)
    cos_a = np.cos(rot_angle)
    sin_a = np.sin(rot_angle)
    R_clear = np.array([
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ], dtype=np.float32)
    h_clear = h_clear @ R_clear.T
    gestures["CLEAR"] = h_clear

    return gestures


def augment_landmarks(
    base_coords: np.ndarray,
    noise_level: float = 0.02,
    rotation_range_deg: float = 12.0,
    scale_range: Tuple[float, float] = (0.88, 1.12)
) -> np.ndarray:
    """
    Applies realistic 3D spatial transformations:
    - 3D Euler rotation matrix (roll, pitch, yaw)
    - Scale variations
    - Additive Gaussian noise per joint
    """
    coords = base_coords.copy()

    # 1. Random 3D Rotation
    angles = np.radians(np.random.uniform(-rotation_range_deg, rotation_range_deg, size=3))
    cx, cy, cz = np.cos(angles)
    sx, sy, sz = np.sin(angles)

    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]], dtype=np.float32)
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]], dtype=np.float32)
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]], dtype=np.float32)
    R = Rz @ Ry @ Rx

    coords = coords @ R.T

    # 2. Scale factor
    scale = np.random.uniform(scale_range[0], scale_range[1])
    coords *= scale

    # 3. Gaussian landmark noise
    noise = np.random.normal(0.0, noise_level, size=coords.shape).astype(np.float32)
    coords += noise

    return coords


def generate_dataset(
    samples_per_class: int = 500,
    output_path: str = "ml_model/data/sign_landmarks_dataset.npz"
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Generates an augmented, highly diverse dataset of features and labels for word gestures.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canonical = define_canonical_gestures()
    class_names = sorted(list(canonical.keys()))

    X_list: List[np.ndarray] = []
    y_list: List[int] = []

    print(f"Generating dataset for {len(class_names)} word classes ({samples_per_class} samples each)...")

    for class_idx, name in enumerate(class_names):
        base_hand = canonical[name]
        for _ in range(samples_per_class):
            aug_coords = augment_landmarks(base_hand)

            # Extract features for canonical hand pose
            feat = LandmarkPreprocessor.extract_features(aug_coords, handedness="Right")
            X_list.append(feat)
            y_list.append(class_idx)

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int32)

    # Save to disk
    np.savez_compressed(
        output_path,
        X=X,
        y=y,
        class_names=np.array(class_names)
    )

    print(f"Dataset generated successfully! Shape: X={X.shape}, y={y.shape}")
    print(f"Classes ({len(class_names)}): {class_names}")
    print(f"Saved to: {output_path}")

    return X, y, class_names


if __name__ == "__main__":
    generate_dataset()
