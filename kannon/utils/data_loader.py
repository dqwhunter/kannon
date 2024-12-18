import pandas as pd

def load_csv_data(file_path):
    """Load a CSV file into a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None