from create_zen_garden_timeline import create_zen_garden_timeline

# Specify the input data and output paths
data_path = "data/project_timeline.csv"
output_path = "output/zen_garden_timeline.png"

# Generate the Zen garden timeline visualization
create_zen_garden_timeline(data_path, output_path)

print(f"Zen garden timeline visualization saved at: {output_path}")