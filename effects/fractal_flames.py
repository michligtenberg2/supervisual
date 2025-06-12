import numpy as np
from matplotlib.patches import Circle

def render(ax, chunk, opacity=0.5, color="#FF6600", strength=0.5):
    energy = np.mean(np.abs(chunk))
    np.random.seed(int(energy * 10000) % 100000)
    # Laat aantal cirkels en grootte afhangen van strength
    n_circles = int(20 + energy * (50 + 200 * strength))
    for _ in range(n_circles):
        r = 0.01 + np.random.rand() * (0.07 + 0.15 * strength)
        x = np.random.normal(0, 0.5)
        y = np.sin(x * np.pi * 2 + energy * 5) * 0.5
        alpha = opacity * (0.2 + 0.8 * np.random.rand())
        circle = Circle((x, y), r, color=color, alpha=alpha, linewidth=0)
        ax.add_patch(circle)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
