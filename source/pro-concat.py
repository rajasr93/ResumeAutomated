import pandas as pd
import os

# Function to filter columns and concatenate dataframes
def concat_dataframes(folder_path):
    # Get list of files in the specified folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    # List to store filtered dataframes
    filtered_dfs = []
    # Iterate through files
    for file in files:
        # Read CSV file into DataFrame
        df = pd.read_csv(os.path.join(folder_path, file))
        # Check if DataFrame has more than 4 columns
        if len(df.columns) > 4:
            # Filter DataFrame to keep only specific columns
            df = df[['title', 'company', 'location', 'description']]
        # Append filtered DataFrame to list
        filtered_dfs.append(df)
    # Concatenate filtered DataFrames
    concatenated_df = pd.concat(filtered_dfs)
    
    # Drop rows with null values in the 'description' column
    concatenated_df = concatenated_df.dropna(subset=['description'])
    
    # Remove duplicate rows
    concatenated_df = concatenated_df.drop_duplicates()
    
    return concatenated_df

# Specify folder path containing finalized data
folder_path = '../finalized_data'

# Concatenate dataframes, drop rows with null values, and remove duplicates
concatenated_df = concat_dataframes(folder_path)
print("Shape of concatenated DataFrame:", concatenated_df.shape)
output_file = '../finalized_data/concatenated_data.csv'
concatenated_df.to_csv(output_file, index=True)
print("Concatenated data saved to:", output_file)
