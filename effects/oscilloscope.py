import numpy as np

def render(ax, chunk, opacity=0.65, color="#00FF99", strength=0.5):
    if len(chunk) == 0:
        return

    chunk = chunk / np.max(np.abs(chunk)) if np.max(np.abs(chunk)) > 0 else chunk
    x = np.linspace(-1, 1, len(chunk))
    y = chunk * (1 + 1.5 * strength)  # amplitude afhankelijk van strength

    # Glow-layer (dikkere, transparante achtergrondlijn)
    ax.plot(x, y, color=color, linewidth=6 + 8 * strength, alpha=opacity * 0.2)

    # Hoofdoscilloscope
    ax.plot(x, y, color=color, linewidth=1.2 + 2 * strength, alpha=opacity)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1.1 - strength, 1.1 + strength)
