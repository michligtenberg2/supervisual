import os
import librosa
import matplotlib.pyplot as plt
import importlib
from tempfile import mkdtemp
import subprocess

def run_visual_engine(input_video, effects, opacity=0.65, fps=30, output="final_output.mp4", color="#FFFFFF"):
    # Stap 1: Audio extraheren
    tempdir = mkdtemp()
    audio_path = os.path.join(tempdir, "temp_audio.wav")
    cmd = ["ffmpeg", "-y", "-i", input_video, "-q:a", "0", "-map", "a", audio_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Stap 2: Audio analyseren
    y, sr = librosa.load(audio_path, sr=44100)
    samples_per_frame = int(sr / fps)
    total_frames = len(y) // samples_per_frame

    # Stap 3: Frames renderen met effecten
    frame_dir = os.path.join(tempdir, "frames")
    os.makedirs(frame_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=100)
    plt.axis("off")

    loaded_effects = []
    for name in effects:
        try:
            mod = importlib.import_module(f"effects.{name}")
            loaded_effects.append(mod)
        except:
            print(f"⚠️ Effect '{name}' niet gevonden")

    print(f"🎨 Rendering {total_frames} frames...")
    for i in range(total_frames):
        ax.clear()
        fig.patch.set_alpha(0.0)
        ax.set_facecolor((0, 0, 0, 0))
        ax.axis("off")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)

        chunk = y[i * samples_per_frame:(i+1) * samples_per_frame]
        for effect in loaded_effects:
            effect.render(ax, chunk, opacity=opacity, color=color)

        fig.canvas.draw()
        frame_path = os.path.join(frame_dir, f"frame_{i:05d}.png")
        fig.savefig(frame_path, dpi=100, transparent=True)

    plt.close()

    # Stap 4: Render overlay video
    overlay = os.path.join(tempdir, "overlay.mp4")
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(frame_dir, "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuva420p",
        overlay
    ]
    subprocess.run(cmd)

    # Stap 5: Compositie met originele video
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-i", overlay,
        "-filter_complex", "[0:v][1:v] overlay=(W-w)/2:(H-h)/2:format=auto",
        "-c:a", "copy",
        output
    ]
    subprocess.run(cmd)

    print(f"✅ Klaar! Bestand opgeslagen als: {output}")

