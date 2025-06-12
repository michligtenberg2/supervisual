import os
import librosa
import matplotlib.pyplot as plt
import importlib
from tempfile import mkdtemp
import subprocess

def run_visual_engine(input_video, effects, opacity=0.65, fps=30, output="final_output.mp4", color="#FFFFFF", bg_color="#000000", strength=0.5, audio_override=None):
    # Stap 1: Audio extraheren
    tempdir = mkdtemp()
    if audio_override:
        audio_path = audio_override
    else:
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
        # Set both ax and fig patch to fully transparent if needed
        if bg_color.lower() in ["transparent", "", "none"]:
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
        for effect in loaded_effects:
            kwargs = {"opacity": opacity, "color": color}
            if "strength" in effect.render.__code__.co_varnames:
                kwargs["strength"] = strength
            effect.render(ax, chunk, **kwargs)

        fig.canvas.draw()
        frame_path = os.path.join(frame_dir, f"frame_{i:05d}.png")
        # Use RGBA PNGs for transparency
        fig.savefig(frame_path, dpi=100, transparent=True)
        # Remove alpha channel from white pixels (post-process)
        if bg_color.lower() in ["transparent", "", "none"]:
            try:
                from PIL import Image
                img = Image.open(frame_path).convert("RGBA")
                datas = img.getdata()
                newData = []
                for item in datas:
                    # If pixel is white, make it fully transparent
                    if item[0] > 250 and item[1] > 250 and item[2] > 250:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)
                img.save(frame_path, "PNG")
            except Exception as e:
                print(f"[WARN] PIL post-process failed: {e}")
        print(f"Frame {i+1}/{total_frames}", flush=True)

    plt.close()

    # Stap 4: Render overlay video
    overlay = os.path.join(tempdir, "overlay.mp4")
    if bg_color.lower() in ["transparent", "", "none"]:
        # Use -vf format=yuva420p to preserve alpha
        cmd = [
            "ffmpeg", "-y", "-framerate", str(fps),
            "-i", os.path.join(frame_dir, "frame_%05d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuva420p",
            overlay
        ]
    else:
        cmd = [
            "ffmpeg", "-y", "-framerate", str(fps),
            "-i", os.path.join(frame_dir, "frame_%05d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            overlay
        ]
    subprocess.run(cmd)

    # Create standard output folder if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.isabs(output):
        output = os.path.join(output_dir, output)

    # Stap 5: Compositie met originele video
    if bg_color.lower() in ["transparent", "", "none"]:
        # Overlay with alpha (transparency)
        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-i", overlay,
            "-filter_complex", "[0:v][1:v] overlay=shortest=1:format=auto",
            "-c:a", "copy",
            output
        ]
    else:
        # Normal overlay
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

def render_effect_preview(audio_path, effect, output_path, fps=30, opacity=0.65, color="#FFFFFF", background="transparent", duration=5, image=None, strength=0.5):
    import numpy as np
    import importlib
    import matplotlib.pyplot as plt
    import librosa
    from PIL import Image
    import subprocess
    import tempfile

    y, sr = librosa.load(audio_path, sr=44100)
    samples_per_frame = int(sr / fps)
    total_frames = int(duration * fps)
    y = y[:total_frames * samples_per_frame]

    frame_dir = tempfile.mkdtemp()
    fig, ax = plt.subplots(figsize=(6.4, 4.8), dpi=100)
    plt.axis("off")

    try:
        mod = importlib.import_module(f"effects.{effect}")
    except Exception as e:
        print(f"⚠️ Effect '{effect}' niet gevonden: {e}")
        return

    print(f"🎨 Rendering {total_frames} preview frames...")
    for i in range(total_frames):
        ax.clear()
        if background.lower() in ["transparent", "", "none"]:
            ax.set_facecolor((0, 0, 0, 0))
            fig.patch.set_facecolor((0, 0, 0, 0))
            fig.patch.set_alpha(0.0)
        else:
            ax.set_facecolor(background)
            fig.patch.set_facecolor(background)
            fig.patch.set_alpha(1.0)
        ax.axis("off")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        chunk = y[i * samples_per_frame:(i+1) * samples_per_frame]
        # Geef image en strength argumenten door als het effect dat ondersteunt
        kwargs = {"opacity": opacity, "color": color}
        if "image_path" in mod.render.__code__.co_varnames:
            kwargs["image_path"] = image
        if "strength" in mod.render.__code__.co_varnames:
            kwargs["strength"] = strength
        mod.render(ax, chunk, **kwargs)
        fig.canvas.draw()
        frame_path = os.path.join(frame_dir, f"frame_{i:05d}.png")
        fig.savefig(frame_path, dpi=100, transparent=True)
        # Remove alpha from white pixels for true transparency
        if background.lower() in ["transparent", "", "none"]:
            try:
                img = Image.open(frame_path).convert("RGBA")
                datas = img.getdata()
                newData = []
                for item in datas:
                    if item[0] > 250 and item[1] > 250 and item[2] > 250:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                img.putdata(newData)
                img.save(frame_path, "PNG")
            except Exception as e:
                print(f"[WARN] PIL post-process failed: {e}")
        print(f"Frame {i+1}/{total_frames}", flush=True)
    plt.close()

    # Render frames to video
    if background.lower() in ["transparent", "", "none"]:
        pix_fmt = "yuva420p"
    else:
        pix_fmt = "yuv420p"
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(frame_dir, "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", pix_fmt, output_path
    ]
    subprocess.run(cmd)
    print(f"✅ Preview video saved: {output_path}")

