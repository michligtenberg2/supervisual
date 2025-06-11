import os
import subprocess

def extract_audio(input_video, out_wav):
    cmd = ["ffmpeg", "-y", "-i", input_video, "-q:a", "0", "-map", "a", out_wav]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def render_overlay_from_frames(frame_dir, fps, output_overlay):
    cmd = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", os.path.join(frame_dir, "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuva420p", output_overlay
    ]
    subprocess.run(cmd)

def composite_overlay(input_video, overlay_video, output_final):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-i", overlay_video,
        "-filter_complex", "[0:v][1:v] overlay=(W-w)/2:(H-h)/2:format=auto",
        "-c:a", "copy",
        output_final
    ]
    subprocess.run(cmd)

def clean_temp(paths):
    for p in paths:
        if os.path.isfile(p):
            os.remove(p)
        elif os.path.isdir(p):
            import shutil
            shutil.rmtree(p)
