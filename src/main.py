import os
import random
import json
import pandas as pd
from get_jobs import JobScraper
from cleaner import JobDataCleaner
from data_annotation import DataAnnotator

class JobDataPipeline:
    def __init__(self, cities, job_titles, api_key_path, sample_size=4):
        self.cities = random.sample(cities, sample_size)
        self.job_titles = random.sample(job_titles, sample_size)
        self.cleaned_data = None
        self.api_key_path = api_key_path

    def run(self):
        # scraper = JobScraper(search_terms=self.job_titles, cities=self.cities)
        # scraper.scrape_jobs()
        # jobs_df = scraper.create_dataframe()
        
        # cleaner = JobDataCleaner(jobs_df)
        # cleaner.remove_null_descriptions()
        # cleaner.clean_descriptions()
        # cleaner.remove_duplicates()
        # cleaned_data = cleaner.get_cleaned_data()
        cleaned_data = pd.read_csv('../data/job_data_cleaned.csv')

        annotator = DataAnnotator(self.api_key_path)
        annotator.load_data(cleaned_data)
        annotator.extract_skills()
        annotated_data = annotator.get_annotated_data()
        self.save_data(annotated_data)

    def save_data(self, cleaned_data):  # Now accepts cleaned_data as a parameter
        if cleaned_data is not None:
            cleaned_data.to_csv('../data/job_data_cleaned.csv', index=False)
            print(f"Cleaned and saved data to job_data_cleaned.csv with {cleaned_data.shape[0]} rows.")
        else:
            print("No data to save.")

if __name__ == "__main__":
    json_file_path = "../data/city_title.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    cities, job_titles =  data['cities'], data['job_titles']
    api_key_path = os.path.join(os.path.dirname(__file__), 'api-key.txt')
    job_data_pipeline = JobDataPipeline(cities, job_titles, api_key_path,sample_size=1)
    job_data_pipeline.run()


