import os
import random
import json
# import pandas as pd
from tqdm import tqdm
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
        try:
            print("Scraping job listings...")
            scraper = JobScraper(search_terms=self.job_titles, cities=self.cities)
            scraper.scrape_jobs()
            jobs_df = scraper.create_dataframe()
        except Exception as e:
            print(f"Error during job scraping: {e}")
            return

        try:
            print("\nCleaning job data...")
            cleaner = JobDataCleaner(jobs_df)
            cleaner.remove_null_descriptions()
            with tqdm(total=len(jobs_df), unit="descriptions", unit_scale=True, unit_divisor=1000, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
                cleaner.clean_descriptions(pbar)
            cleaner.remove_duplicates()
            cleaned_data = cleaner.get_cleaned_data()
        except Exception as e:
            print(f"Error during job data cleaning: {e}")
            return

        try:
            print("\nAnnotating job data...")
            annotator = DataAnnotator(self.api_key_path)
            annotator.load_data(cleaned_data)
            annotated_data, failure_points = annotator.annotate_data()
        except Exception as e:
            print(f"Error during data annotation: {e}")
            annotated_data = None
            print("Saving Cleaned data without annotations...")
            self.save_data(cleaned_data)
            failure_points = []

        try:
            self.save_data(annotated_data)
        except Exception as e:
            print(f"Error during saving data: {e}")

        try:
            self.save_failure_points(failure_points)
        except Exception as e:
            print(f"Error saving failure points: {e}")

    def save_data(self, cleaned_data):
        if cleaned_data is not None:
            cleaned_data.to_csv('../data/job_data_cleaned.csv', index=False)
            print(f"\nCleaned and saved data to job_data_cleaned.csv with {cleaned_data.shape[0]} rows.")
        else:
            print("No data to save.")

    def save_failure_points(self, failure_points):
        if failure_points:
            with open('../data/failure_points.json', 'w') as file:
                json.dump(failure_points, file)
            print(f"\nFailure points saved to failure_points.json with {len(failure_points)} points.")

if __name__ == "__main__":
    json_file_path = "../data/city_title.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    cities, job_titles = data['cities'], data['job_titles']
    api_key_path = os.path.join(os.path.dirname(__file__), 'api-key.txt')
    job_data_pipeline = JobDataPipeline(cities, job_titles, api_key_path, sample_size=50)
    job_data_pipeline.run()

