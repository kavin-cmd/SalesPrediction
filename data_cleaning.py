# data_cleaning.py

import os
import re
import pandas as pd

# Cleaning data
def clean_data(data_frames):
    # Merge all data frames into one
    df_all = pd.concat(data_frames, ignore_index=True)
    
    # Copy the merged data for cleaning
    df_all_clean = df_all.copy()
    
    # Remove NaN values
    df_all_clean = df_all_clean.dropna()
    
    # Rename columns
    df_all_clean.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
    
    # Remove rows with erroneous data
    df_all_clean = df_all_clean[df_all_clean.quantity_ordered != "Quantity Ordered"]
    
    # Convert data types
    df_all_clean['quantity_ordered'] = pd.to_numeric(df_all_clean['quantity_ordered'], errors='coerce')
    df_all_clean['price_each'] = pd.to_numeric(df_all_clean['price_each'], errors='coerce')
    
    # Specify date format explicitly
    df_all_clean['order_date'] = pd.to_datetime(df_all_clean['order_date'], format='%m/%d/%y %H:%M', errors='coerce')
    
    # Remove any rows with conversion errors
    df_all_clean = df_all_clean.dropna()
    
    # Create new columns
    df_all_clean['month'] = df_all_clean.order_date.dt.month_name()
    df_all_clean['total_sales'] = df_all_clean.quantity_ordered * df_all_clean.price_each
    
    pattern = r'(?:St,\s)(\w+\s?\w+\s?\w+\s?,\s\w+)'
    df_all_clean['city'] = df_all_clean.purchase_address.str.extract(pattern)
    
    df_all_clean['hour'] = df_all_clean.order_date.dt.hour
    
    return df_all_clean

if __name__ == "__main__":
    from data_gathering import gather_data
    
    # Ensure the output directory exists
    output_dir = 'SalesPrediction/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    data_frames = gather_data()
    cleaned_data = clean_data(data_frames)
    cleaned_data.to_csv(os.path.join(output_dir, 'all_data_master.csv'), index=False)
    print(f"Cleaned data saved to '{output_dir}/all_data_master.csv'")
