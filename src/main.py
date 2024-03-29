import os
import random
import json
import pandas as pd
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
        print("Scraping job listings...")
        scraper = JobScraper(search_terms=self.job_titles, cities=self.cities)
        scraper.scrape_jobs()
        jobs_df = scraper.create_dataframe()

        print("\nCleaning job data...")
        cleaner = JobDataCleaner(jobs_df)
        cleaner.remove_null_descriptions()
        with tqdm(total=len(jobs_df), unit="descriptions", unit_scale=True, unit_divisor=1000, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
            cleaner.clean_descriptions(pbar)
        cleaner.remove_duplicates()
        cleaned_data = cleaner.get_cleaned_data()
        print(cleaned_data)

        print("\nAnnotating job data...")
        try:
            annotator = DataAnnotator(self.api_key_path)
            annotator.load_data(cleaned_data.head(5))
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
    json_file_path = "../data/city_title.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    sample_size = 10
    cities, job_titles = data['cities'], data['job_titles']
    api_key_path = os.path.join(os.path.dirname(__file__), 'api-key.txt')
    job_data_pipeline = JobDataPipeline(cities, job_titles, api_key_path, sample_size=sample_size)
    job_data_pipeline.run()

if __name__ == "__main__":
    main()




