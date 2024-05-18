import os
import pandas as pd

# 2. Gathering data
def gather_data(data_dir='SalesPrediction/data'):
    file_list = os.listdir(data_dir)
    data_frames = []

    for file in file_list:
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(data_dir, file))
            data_frames.append(df)

    return data_frames

if __name__ == "__main__":
    data_frames = gather_data()
    print(f"Gathered {len(data_frames)} data frames.")
