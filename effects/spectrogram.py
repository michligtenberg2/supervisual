import numpy as np
import librosa.display

def render(ax, chunk, opacity=0.8, color="#00FFFF", strength=0.5):
    if len(chunk) == 0:
        return
    # Laat n_fft en kleur afhangen van strength
    n_fft = int(128 + 384 * strength)  # van 128 tot 512
    hop_length = int(n_fft // (2 + 2 * strength))
    S = np.abs(librosa.stft(chunk, n_fft=n_fft, hop_length=hop_length))**2
    S_db = librosa.power_to_db(S, ref=np.max)
    # Kleurintensiteit via strength
    import matplotlib
    base_cmap = matplotlib.cm.get_cmap("viridis")
    alpha = opacity * (0.7 + 0.6 * strength)
    ax.imshow(
        S_db,
        cmap=base_cmap,
        origin="lower",
        aspect="auto",
        extent=[-1, 1, -1, 1],
        alpha=alpha
    )
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis("off")
