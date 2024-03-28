import pandas as pd
import os

class DataFrameConcatenator:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_file_list(self):
        files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]
        return files

    def filter_dataframe(self, df):
        if len(df.columns) > 4:
            df = df[['title', 'company', 'location', 'description']]
        return df

    def concat_dataframes(self):
        file_list = self.get_file_list()
        filtered_dfs = []

        for file in file_list:
            df = pd.read_csv(os.path.join(self.folder_path, file))
            filtered_df = self.filter_dataframe(df)
            filtered_dfs.append(filtered_df)

        concatenated_df = pd.concat(filtered_dfs)
        concatenated_df = concatenated_df.dropna(subset=['description'])
        concatenated_df = concatenated_df.drop_duplicates()

        return concatenated_df

    def save_concatenated_dataframe(self, output_file):
        concatenated_df = self.concat_dataframes()
        concatenated_df.to_csv(output_file, index=True)
        print(f"Shape of concatenated DataFrame: {concatenated_df.shape}")
        print(f"Concatenated data saved to: {output_file}")

if __name__ == "__main__":
    folder_path = '../finalized_data'
    output_file = '../finalized_data/concatenated_data.csv'

    concatenator = DataFrameConcatenator(folder_path)
    concatenator.save_concatenated_dataframe(output_file)