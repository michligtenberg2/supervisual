import numpy as np
from PIL import Image
import os
import cv2

def render(ax, chunk, opacity=0.85, color="#FFFFFF", image_path=None, strength=0.5):
    # 1. Foto laden en vervormen op basis van audio RMS en strength
    if image_path and os.path.exists(image_path):
        img = Image.open(image_path).convert("RGBA")
        img_np = np.array(img)
        rms = np.sqrt(np.mean(chunk**2))
        # strength bepaalt de maximale vervorming
        s = np.clip(strength, 0.0, 1.0)
        max_strength = 0.25 + s * 1.25  # van 0.25 tot 1.5
        max_amp = 10 + s * 90           # van 10 tot 100
        cur_strength = min(max_strength * rms, 1.5)
        amp = max_amp * rms
        h, w = img_np.shape[:2]
        map_y, map_x = np.indices((h, w), dtype=np.float32)
        freq = 2 + 8 * cur_strength
        map_x += (np.sin(map_y / h * np.pi * freq) * amp).astype(np.float32)
        try:
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA)
            warped = cv2.remap(img_cv, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            warped = cv2.cvtColor(warped, cv2.COLOR_BGRA2RGBA)
            img = Image.fromarray(warped, 'RGBA')
        except Exception as e:
            pass
        ax.imshow(img, extent=[-1.2, 1.2, -1.2, 1.2], aspect='auto', alpha=0.7, zorder=0)
    # 2. Spectrogram overlay
    import librosa, matplotlib.colors
    S = np.abs(librosa.stft(chunk, n_fft=256, hop_length=64))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    cmap = 'magma'
    ax.imshow(S_db, aspect='auto', origin='lower', cmap=cmap, alpha=opacity, extent=[-1.2, 1.2, -1.2, 1.2], zorder=1)
    ax.axis('off')
