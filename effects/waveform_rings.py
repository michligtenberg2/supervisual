import numpy as np

def render(ax, chunk, opacity=0.65, color="#FFFFFF", strength=0.5):
    if len(chunk) == 0:
        return

    chunk = chunk / np.max(np.abs(chunk)) if np.max(np.abs(chunk)) > 0 else chunk
    theta = np.linspace(0, 2 * np.pi, len(chunk))
    # Laat ringgrootte en lijndikte afhangen van strength
    base = 0.6 + 0.6 * strength
    scale = 0.3 + 0.5 * strength
    radius = base + scale * chunk
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    lw = 1.5 + 3 * strength
    ax.plot(x, y, color=color, linewidth=lw, alpha=opacity)
    ax.set_aspect('equal')
