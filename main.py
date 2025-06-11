import argparse
from engine import run_visual_engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🎛️ Supervisual Engine - combineer audio-visualisaties over video")
    parser.add_argument("input", help="Pad naar input .mp4 bestand")
    parser.add_argument("--effects", help="Effecten (bijv: lissajous,waveform_rings,ascii)", default="lissajous")
    parser.add_argument("--opacity", type=float, default=0.65, help="Transparantie (0.0 - 1.0)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per seconde")
    parser.add_argument("--color", default="#FFFFFF", help="Kleur van visualisatie (hex)")
    parser.add_argument("--output", default="final_output.mp4", help="Bestandsnaam output video")
    parser.add_argument("--background", default="#000000", help="Achtergrondkleur (hex)")
   
    args = parser.parse_args()

    run_visual_engine(
        input_video=args.input,
        effects=args.effects.split(","),
        opacity=args.opacity,
        fps=args.fps,
        color=args.color,
        output=args.output
        bg_color
    )
