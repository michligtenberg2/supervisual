# 🎬 Supervisual MegaTool Suite

**Supervisual MegaTool Suite** is a desktop app for creating audio-reactive videos and images. Everything is bundled into one interface, with tabs for different tasks and a live preview.

> 🇳🇱 [Lees dit in het Nederlands](README.md)

## Features

- **Multiple workflows in one app**  
  Tabs for:
  - Video Effects  
  - Photo Spectrograms  
  - MP4 Previews  
  - Merging MP4s

- **Audio-reactive visuals**  
  Effects respond to the audio you select.

- **Supports both video and still images**  
  Works with static images or video + external audio.

- **Live preview**  
  Quickly check a short preview of your settings.

- **Effect settings**  
  Adjust color, intensity, transparency, and more via sliders and color pickers.

- **Batch or single render**  
  Process one file or multiple at once.

- **Output and progress**  
  Set output file name and folder. Progress bar and log are always visible.

## Tabs

- **Video Effect** – Add a visual effect to a video.
- **Photo Spectrogram** – Turn a photo into a short video with spectrogram.
- **MP4 Preview** – Generate a quick MP4 preview of your effect.
- **Merge MP4s** – Combine several MP4 files into one seamless video.

## Available Effects

- Lissajous  
- Waveform Rings  
- Oscilloscope  
- Fractal Flames  
- Spectrogram  
- Pulse Flashes  
- ASCII  
- Matrix Rain  
- Rotating Shapes  
- Photo Spectrogram (with face warping)

## Installation

```bash
git clone https://github.com/michligtenberg2/supervisual.git
cd supervisual
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Folder structure

- `gui/` – GUI code (PyQt6)  
- `engine/` – Core logic for rendering  
- `effects/` – All visual effect modules  
- `output/` – Rendered output files  
- `previews/` – Preview clips

## Notes

- Output files are saved to the correct folder by default (unless changed manually).
- Progress bar and log window are always visible at the bottom.

---

Using the app? Found a bug? Got ideas? Feel free to open an issue on GitHub.