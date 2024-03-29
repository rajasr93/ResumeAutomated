import pandas as pd
import re
from tqdm import tqdm

class JobDataCleaner:
    def __init__(self, dataframe):
        """
        Initializes the JobDataCleaner with a DataFrame.
        :param dataframe: A pandas DataFrame containing job listings.
        """
        self.dataframe = dataframe

    def remove_null_descriptions(self):
        """
        Removes any rows with null values in the 'description' column.
        """
        self.dataframe.dropna(subset=['description'], inplace=True)

    def clean_descriptions(self, pbar=None):
        """
        Cleans the 'description' column by removing special characters, newline characters,
        and converting multiple spaces to a single space, preparing it for text processing.
        Optionally updates a progress bar (pbar) if provided.
        """
        if self.dataframe is not None:
            pattern = r'[^\w\s]'
            for i in self.dataframe.index:
                # Perform cleaning on each description
                description = self.dataframe.at[i, 'description'].lower()
                description = re.sub(pattern, '', description).replace('\n', ' ')
                description = re.sub(r'\s+', ' ', description).strip()
                self.dataframe.at[i, 'description'] = description
                
                # Update the progress bar if it's provided
                if pbar is not None:
                    pbar.update(1)
        else:
            print("Dataframe not loaded. Cannot clean descriptions.")

    def remove_duplicates(self):
        """
        Removes duplicate rows based on the 'description' column, as well as
        rows with the same 'title' and 'company' combination.
        """
        self.dataframe.drop_duplicates(subset=['description'], inplace=True)
        self.dataframe.drop_duplicates(subset=['title', 'company'], inplace=True)

    def get_cleaned_data(self):
        """
        Returns the cleaned DataFrame.
        """
        return self.dataframe
