import os
import sys
import librosa
import numpy as np
import matplotlib.pyplot as plt
from effects import lissajous, waveform_rings, oscilloscope, fractal_flames, spectrogram, pulse_flashes, ascii, matrix_rain, rotating_shapes
from PIL import Image
import subprocess

def render_preview(effect_func, audio_path, out_gif, duration=2.0, fps=15, color="#FFFFFF", bg_color="transparent"):
    y, sr = librosa.load(audio_path, sr=44100)
    samples_per_frame = int(sr / fps)
    total_frames = int(duration * fps)
    y = y[:total_frames * samples_per_frame]
    frames = []
    fig, ax = plt.subplots(figsize=(3, 2), dpi=80)
    for i in range(total_frames):
        ax.clear()
        if bg_color == "transparent":
            ax.set_facecolor((0, 0, 0, 0))
            fig.patch.set_facecolor((0, 0, 0, 0))
            fig.patch.set_alpha(0.0)
        else:
            ax.set_facecolor(bg_color)
            fig.patch.set_facecolor(bg_color)
            fig.patch.set_alpha(1.0)
        ax.axis("off")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        chunk = y[i * samples_per_frame:(i+1) * samples_per_frame]
        effect_func(ax, chunk, opacity=0.85, color=color)
        fig.canvas.draw()
        # Save to buffer
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        img = img[..., [1,2,3,0]]  # ARGB to RGBA
        pil_img = Image.fromarray(img, 'RGBA')
        frames.append(pil_img)
    plt.close(fig)
    frames[0].save(out_gif, save_all=True, append_images=frames[1:], duration=int(1000/fps), loop=0, disposal=2, transparency=0)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Quick preview GIF generator for effects.")
    parser.add_argument("effect", help="Effect name (e.g. lissajous)")
    parser.add_argument("audio", help="Input .mp3 or .wav file")
    parser.add_argument("output", help="Output .gif file")
    parser.add_argument("--duration", type=float, default=2.0, help="Duration in seconds")
    parser.add_argument("--fps", type=int, default=15, help="Frames per second")
    parser.add_argument("--color", default="#FFFFFF", help="Effect color")
    parser.add_argument("--bg", default="transparent", help="Background color or 'transparent'")
    args = parser.parse_args()

    effect_map = {
        "lissajous": lissajous.render,
        "waveform_rings": waveform_rings.render,
        "oscilloscope": oscilloscope.render,
        "fractal_flames": fractal_flames.render,
        "spectrogram": spectrogram.render,
        "pulse_flashes": pulse_flashes.render,
        "ascii": ascii.render,
        "matrix_rain": matrix_rain.render,
        "rotating_shapes": rotating_shapes.render,
    }
    if args.effect not in effect_map:
        print(f"Effect '{args.effect}' not found.")
        sys.exit(1)
    render_preview(effect_map[args.effect], args.audio, args.output, args.duration, args.fps, args.color, args.bg)
    print(f"GIF saved to {args.output}")

if __name__ == "__main__":
    main()
