import os
import random
import json
import pandas as pd
from tqdm import tqdm
from get_jobs import JobScraper
from cleaner import JobDataCleaner
from data_annotation import DataAnnotator

class JobDataPipeline:
    def __init__(self, cities, job_titles, api_key_path, sample_size=4, results_wanted_per_combination=1000):
        self.cities = random.sample(cities, sample_size)
        self.job_titles = random.sample(job_titles, sample_size)
        self.cleaned_data = None
        self.api_key_path = api_key_path
        self.results_wanted_per_combination = results_wanted_per_combination

    def run(self):
        print("Scraping job listings...")
        scraper = JobScraper(search_terms=self.job_titles, cities=self.cities, results_wanted_per_combination=self.results_wanted_per_combination)
        with tqdm(total=len(self.cities) * len(self.job_titles), unit="combinations", unit_scale=True, unit_divisor=1000, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
            scraper.scrape_jobs(pbar)
            jobs_df = scraper.create_dataframe()

        print("\nCleaning job data...")
        cleaner = JobDataCleaner(jobs_df)
        cleaner.remove_null_descriptions()
        with tqdm(total=len(jobs_df), unit="descriptions", unit_scale=True, unit_divisor=1000, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
            cleaner.clean_descriptions(pbar)
            cleaner.remove_duplicates()
            cleaned_data = cleaner.get_cleaned_data()
            print(cleaned_data)
        print(f"Cleaned data has {cleaned_data.shape[0]} rows.")
        print("Saving cleaned data to job_data_cleaned.csv...")
        cleaned_data.to_csv('../data/job_data_cleaned.csv', index=False)

        print("\nAnnotating job data...")
        try:
            annotator = DataAnnotator(self.api_key_path)
            annotator.load_data(cleaned_data)
            annotated_data = annotator.annotate_data()
            self.save_data(annotated_data)
        except Exception as e:
            print(f"Error: {e} saving the cleaned data without annotations.")
            cleaned_data.to_csv('../data/job_data_cleaned.csv', index=False)

    def save_data(self, cleaned_data):
        if cleaned_data is not None:
            annotated_df, failed_annotations = cleaned_data
            if annotated_df is not None:
                annotated_df.to_csv('../data/annotated_data.csv', index=False, header=True)
                print(f"\nCleaned and saved data to annotated_data.csv with {annotated_df.shape[0]} rows.")
            else:
                print("No data to save.")
        else:
            print("No data to save.")

def main():
    json_file_path = "scity_title.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    # give a sample size less than 18 to avoid any errors sorry about that
    # give a results_wanted_per_combination less than 500 (coz it will take a lot of time to scrape the data)
    sample_size = 1
    results_wanted_per_combination = 50
    cities, job_titles = data['cities'], data['job_titles']
    api_key_path = os.path.join(os.path.dirname(__file__), 'api-key.txt')
    job_data_pipeline = JobDataPipeline(cities, job_titles, api_key_path, sample_size=sample_size, results_wanted_per_combination=results_wanted_per_combination)
    job_data_pipeline.run()

if __name__ == "__main__":
    main()




