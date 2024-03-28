import pandas as pd
import os

class DataProcessor:
    def __init__(self, data_folder, output_folder):
        self.data_folder = data_folder
        self.output_folder = output_folder

    def read_files(self, file_prefix):
        files = [f for f in os.listdir(self.data_folder) if f.startswith(file_prefix)]
        dfs = []
        for file in files:
            file_path = os.path.join(self.data_folder, file)
            df = pd.read_csv(file_path)
            dfs.append(df)
        return dfs

    def concatenate_dataframes(self, dfs):
        concatenated_df = pd.concat(dfs)
        return concatenated_df

    def filter_columns(self, df, columns):
        filtered_df = df[columns]
        return filtered_df

    def save_dataframe(self, df, output_file):
        output_path = os.path.join(self.output_folder, output_file)
        df.to_csv(output_path, index=False)
        print(f"DataFrame saved to: {output_path}")

    def process_data(self, file_prefix, output_file, columns):
        dfs = self.read_files(file_prefix)
        concatenated_df = self.concatenate_dataframes(dfs)
        filtered_df = self.filter_columns(concatenated_df, columns)
        self.save_dataframe(filtered_df, output_file)

if __name__ == "__main__":
    data_folder = '../data'
    output_folder = '../finalized_data'
    file_prefix = 'jobs'
    output_file = 'financial_analyst_job.csv'
    columns = ['title', 'company', 'location', 'description']

    data_processor = DataProcessor(data_folder, output_folder)
    data_processor.process_data(file_prefix, output_file, columns)