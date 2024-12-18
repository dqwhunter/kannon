def apply_japanese_style(plt):
    """Apply a simple Japanese aesthetic to Matplotlib plots."""
    plt.style.use("seaborn-muted")
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 12,
        "axes.edgecolor": "gray",
        "axes.linewidth": 1,
        "grid.color": "lightgray",
        "grid.linestyle": "--",
        "grid.linewidth": 0.5,
    })