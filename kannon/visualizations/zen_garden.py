import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Circle
from datetime import datetime

def create_zen_garden_timeline(data_path, output_path):
    data = pd.read_csv(data_path)
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])
    data['duration'] = (data['end_date'] - data['start_date']).dt.days

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1, len(data) + 1)
    ax.set_ylim(0, max(data['duration']) + 10)
    ax.axis('off')

    for i, row in data.iterrows():
        x = i
        y = row['duration']
        status = row['status']
        ax.plot([x, x], [0, y], color="gray", linewidth=2, linestyle="dashed")
        color = {"Completed": "black", "In Progress": "blue", "Pending": "red"}[status]
        stone = Circle((x, y), 0.5, color=color)
        ax.add_patch(stone)
        ax.text(x, y + 2, row['task'], ha='center', va='bottom', fontsize=10)

    ax.legend(
        [Circle((0, 0), 0.5, color="black"), Circle((0, 0), 0.5, color="blue"), Circle((0, 0), 0.5, color="red")],
        ["Completed", "In Progress", "Pending"],
        loc="lower left",
        frameon=False,
    )

    plt.title("Zen Garden Project Timeline", fontsize=14, weight="bold")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()