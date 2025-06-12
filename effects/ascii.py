import numpy as np

def render(ax, chunk, opacity=1.0, color="#FFFFFF", strength=0.5):
    chars = " .:-=+*#%@"
    num_cols = 28
    num_rows = 14
    block = chunk[:num_cols * num_rows]
    if len(block) < num_cols * num_rows:
        block = np.pad(block, (0, num_cols * num_rows - len(block)))

    normed = np.abs(block / np.max(np.abs(block))) if np.max(np.abs(block)) != 0 else block
    levels = (normed * (len(chars)-1)).astype(int)
    grid = np.array([chars[i] for i in levels]).reshape((num_rows, num_cols))

    ax.set_xlim(0, num_cols)
    ax.set_ylim(0, num_rows)
    ax.axis("off")
    ax.set_facecolor((0, 0, 0, 0))

    fontsize = 6 + 10 * strength
    for y in range(num_rows):
        for x in range(num_cols):
            ax.text(
                x + 0.5,
                num_rows - y - 0.5,
                grid[y, x],
                color=color,
                ha="center",
                va="center",
                fontsize=fontsize,
                alpha=opacity,
                family="monospace"
            )
