import os
import pandas as pd

class DataCleaner:
    def __init__(self, data):
        self.data = data

    def clean_data(self):
        self.data = self.data.dropna()
        self.data = self.data.drop_duplicates()
        self.data = self.data.reset_index(drop=True)
        return self.data

class Backup:
    def __init__(self, data_folder, output_file):
        self.data_folder = data_folder
        self.output_file = output_file
        self.dataframes = []

    def read_csv_files(self):
        csv_files = [file for file in os.listdir(self.data_folder) if file.endswith(".csv")]
        for file in csv_files:
            file_path = os.path.join(self.data_folder, file)
            try:
                df = pd.read_csv(file_path)
                cleaner = DataCleaner(df)
                cleaned_df = cleaner.clean_data()
                self.dataframes.append(cleaned_df)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

    def combine_data(self):
        self.read_csv_files()
        combined_data = pd.concat(self.dataframes)
        combined_data.to_csv(self.output_file, index=False)