import os
import pandas as pd

directory = "../data/"
total_rows = 0

for root, dirs, files in os.walk(directory):  # go through all dirs and files
    for filename in files:
        if filename.endswith(".csv"):
            file_path = os.path.join(root, filename)
            df = pd.read_csv(file_path)
            num_rows = len(df.index)
            print(f"{file_path}: {num_rows} rows")
            total_rows += num_rows


print(f"Total rows: {total_rows}")
