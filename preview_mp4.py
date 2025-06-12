import os
import sys
import argparse
import subprocess
import tempfile
from engine import render_effect_preview

# --- CONFIG ---
PREVIEW_DURATION = 5  # seconds
FPS = 30
OPACITY = 0.65
DEFAULT_COLOR = "#FFFFFF"
DEFAULT_BG = "#000000"
PREVIEW_DIR = "previews"


def main():
    parser = argparse.ArgumentParser(description="Generate a short MP4 preview of an effect with audio.")
    parser.add_argument("audio", help="Path to audio file (.mp3 or .wav)")
    parser.add_argument("effect", help="Effect name (matches effects/*.py)")
    parser.add_argument("--color", default=DEFAULT_COLOR, help="Effect color (hex)")
    parser.add_argument("--background", default=DEFAULT_BG, help="Background color (hex or 'transparent')")
    parser.add_argument("--output", default=None, help="Output mp4 path (default: previews/<effect>_preview.mp4)")
    parser.add_argument("--transparent", action="store_true", help="Use transparent background")
    parser.add_argument("--image", default=None, help="Path to image for photo-based effects (optional)")
    parser.add_argument("--strength", type=float, default=0.5, help="Effect strength (0.0 - 1.0)")
    args = parser.parse_args()

    os.makedirs(PREVIEW_DIR, exist_ok=True)
    outname = args.output or os.path.join(PREVIEW_DIR, f"{args.effect}_preview.mp4")

    # Render effect frames to temp video (no audio)
    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "preview.mp4")
        render_effect_preview(
            audio_path=args.audio,
            effect=args.effect,
            output_path=video_path,
            fps=FPS,
            opacity=OPACITY,
            color=args.color,
            background="transparent" if args.transparent else args.background,
            duration=PREVIEW_DURATION,
            image=args.image,
            strength=args.strength
        )

        # Use ffmpeg to trim audio and mux with video
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-ss", "0", "-t", str(PREVIEW_DURATION),
            "-i", args.audio,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-shortest",
            outname
        ]
        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)
        print(f"✅ Preview saved: {outname}")

if __name__ == "__main__":
    main()
