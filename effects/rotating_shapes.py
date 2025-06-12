import numpy as np
from matplotlib.patches import RegularPolygon, Circle

def render(ax, chunk, opacity=0.7, color="#00CCFF", strength=0.5):
    energy = np.mean(np.abs(chunk))
    if energy == 0:
        return

    np.random.seed(int(energy * 100000) % 100000)
    # Laat aantal shapes en grootte afhangen van strength
    n_shapes = 3 + int(3 * strength)
    angles = np.linspace(0, 2*np.pi, n_shapes, endpoint=False)

    for i, angle in enumerate(angles):
        x = 0.6 * np.cos(angle)
        y = 0.6 * np.sin(angle)
        sides = 3 + (i % 4)  # wisselt tussen driehoek, vierkant, vijfhoek, zeshoek
        rot = (energy * 360 + i * 45) % 360
        radius = 0.15 + 0.1 * energy + 0.15 * strength

        shape = RegularPolygon(
            (x, y),
            numVertices=sides,
            radius=radius,
            orientation=np.deg2rad(rot),
            color=color,
            alpha=opacity,
            linewidth=0
        )
        ax.add_patch(shape)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
