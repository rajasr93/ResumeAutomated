import pandas as pd
import re

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

    def clean_descriptions(self):
        """
        Cleans the 'description' column by removing special characters and
        newline characters, preparing it for text processing.
        """
        pattern = r'[^\w\s]'
        self.dataframe['description'] = self.dataframe['description'].str.lower()
        self.dataframe['description'] = self.dataframe['description'].apply(
            lambda x: re.sub(pattern, '', x).replace('\n', ' ')
        )

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
