import numpy as np

def render(ax, chunk, opacity=0.7, color="#00FF00", strength=0.5):
    energy = np.mean(np.abs(chunk))
    np.random.seed(int(energy * 100000) % 100000)

    cols = 20
    rows = 15
    density = int(energy * (50 + 200 * strength))

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.axis("off")
    ax.set_facecolor((0, 0, 0, 0))

    chars = "01⟐▣◉◎◍●◌"  # matrix-achtige mix

    for _ in range(density):
        x = np.random.randint(0, cols)
        y = np.random.randint(0, rows)
        symbol = np.random.choice(list(chars))
        fontsize = 6 + int(energy * 5) + int(10 * strength)
        ax.text(
            x + 0.5, rows - y - 0.5, symbol,
            fontsize=fontsize,
            color=color,
            alpha=opacity * np.random.rand(),
            ha="center",
            va="center",
            family="monospace"
        )
