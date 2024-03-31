import os
import random
import json
import logging
import pandas as pd
from tqdm import tqdm
from get_jobs import JobScraper
from cleaner import JobDataCleaner
import concurrent.futures
from data_annotation import DataAnnotator
from backup import Backup

class JobDataPipeline:
    def __init__(self, cities, job_titles, api_key_path, sample_size=4, results_wanted_per_combination=500):
        self.cities = random.sample(cities, sample_size)
        self.job_titles = random.sample(job_titles, sample_size)
        self.cleaned_data = None
        self.api_key_path = api_key_path
        self.results_wanted_per_combination = results_wanted_per_combination

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def scrape_jobs(self):
        try:
            print("Scraping job listings...")
            print(f"Scraping {len(self.cities) * len(self.job_titles)} combinations of cities and job titles.")
            scraper = JobScraper(search_terms=self.job_titles, cities=self.cities, results_wanted_per_combination=self.results_wanted_per_combination)
            with tqdm(total=len(self.cities) * len(self.job_titles), unit="combinations", unit_scale=True, unit_divisor=1000, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:
                scraper.scrape_jobs(pbar)
                jobs_df = scraper.create_dataframe()
                jobs_df.to_csv('../data/job_data_scraped.csv', index=False)
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
            jobs_df = None
        return jobs_df

    def clean_data(self, jobs_df):
        try:
            print("\nCleaning job data...")
            cleaner = JobDataCleaner(jobs_df)
            cleaner.remove_null_descriptions()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(cleaner.clean_descriptions)
                future.result()
            cleaner.remove_duplicates()
            cleaned_data = cleaner.get_cleaned_data()
            print(f"Cleaned data has {cleaned_data.shape[0]} rows.")
            print("Saving cleaned data to job_data_cleaned.csv...")
            cleaned_data.to_csv('../data/job_data_cleaned.csv', index=False)
        except Exception as e:
            logging.error(f"Error during cleaning: {e}")
            cleaned_data = None
        return cleaned_data

    def annotate_data(self, cleaned_data):
        print("\nAnnotating job data...")
        try:
            annotator = DataAnnotator(self.api_key_path)
            annotator.load_data(cleaned_data)
            annotated_data, _ = annotator.annotate_data()  # Ignore failed annotations
            self.save_data(annotated_data)
        except Exception as e:
            logging.error(f"Error during annotation: {e}")
            print("Saving the cleaned data without annotations.")
            cleaned_data.to_csv('../data/job_data_cleaned.csv', index=False)
    
    def run(self):
        try:
            # jobs_df = self.scrape_jobs()
            # if jobs_df is not None:
            #    cleaned_data = self.clean_data(jobs_df)
            #    if cleaned_data is not None:
            #        self.annotate_data(cleaned_data)
            #else:
            #    logging.error("Scraping step failed. Skipping cleaning and annotation.")
            data_folder = "../data/job_data_cleaned2.csv"
            cleaned_data = pd.read_csv(data_folder)
            if cleaned_data is not None:
                self.annotate_data(cleaned_data)
            else:
                logging.error("Cleaning step failed. Skipping annotation.")
        except Exception as e:
            logging.error(f"Error during pipeline execution: {e}")
            data_folder = "../data/ind_data"
            output_file = "../data/cleaned_backup_data.csv"
            combiner = Backup(data_folder, output_file)
            combiner.combine_data()
            logging.warning("Using backup data for cleaning and annotation.")
            jobs_df = pd.read_csv('../data/cleaned_backup_data.csv')
            cleaned_data = self.clean_data(jobs_df)
            if cleaned_data is not None:
                self.annotate_data(cleaned_data)
            else:
                logging.error("Cleaning step failed. Skipping annotation.")

    def save_data(self, annotated_df):
        if annotated_df is not None:
            annotated_df.to_csv('../data/annotated_data.csv', index=False, header=True)
            print(f"\nCleaned and saved data to annotated_data.csv with {annotated_df.shape[0]} rows.")
        else:
            logging.warning("No data to save.")

def main():
    json_file_path = "../data/city_title.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    # give a sample size less than 18 to avoid any errors sorry about that
    # give a results_wanted_per_combination less than 500 (coz it will take a lot of time to scrape the data)
    sample_size = 5
    results_wanted_per_combination = 1000
    cities, job_titles = data['cities'], data['job_titles']
    api_key_path = os.path.join(os.path.dirname(__file__), 'api-key.txt')
    job_data_pipeline = JobDataPipeline(cities, job_titles, api_key_path, sample_size=sample_size, results_wanted_per_combination=results_wanted_per_combination)
    job_data_pipeline.run()

if __name__ == "__main__":
    main()
