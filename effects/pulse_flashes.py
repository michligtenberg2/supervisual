import numpy as np

def render(ax, chunk, opacity=0.6, color="#FFFFFF", strength=0.5):
    energy = np.mean(np.abs(chunk))
    flash_threshold = 0.2 + 0.6 * (1 - strength)  # lager bij hogere strength
    if energy > flash_threshold:
        ax.set_facecolor(color)
        ax.patch.set_alpha(min(opacity * (energy * (1.5 + 2 * strength)), 1.0))
    else:
        ax.set_facecolor((0, 0, 0, 0))
