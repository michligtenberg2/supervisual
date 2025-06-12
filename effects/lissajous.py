import numpy as np

def render(ax, chunk, opacity=0.65, color="#FFFFFF", strength=0.5):
    t = np.linspace(0, 2 * np.pi, len(chunk))
    # Laat amplitude en lijndikte afhangen van strength
    amp = np.clip(np.abs(chunk).mean() * (3 + 7 * strength), 0.5, 2.5 + 3 * strength)
    lw = 2 + 4 * strength
    x = np.sin(3 * t + amp)
    y = np.sin(4 * t)
    ax.plot(x, y, color=color, linewidth=lw, alpha=opacity)
