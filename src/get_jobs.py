from jobspy import scrape_jobs
import pandas as pd
from tqdm import tqdm
import os

class JobScraper:
    def __init__(self, search_terms, cities, country_indeed='USA', description_format='markdown', results_wanted_per_combination=1000):
        self.search_terms = search_terms  # Updated to be plural, expecting a list of search terms (job titles)
        self.cities = cities
        self.country_indeed = country_indeed
        self.description_format = description_format
        self.results_wanted_per_combination = results_wanted_per_combination

    def scrape_jobs(self, pbar=None):
        total_combinations = len(self.cities) * len(self.search_terms)
        for city in self.cities:
            for search_term in self.search_terms:
                print(f"Scraping {search_term} jobs for {city}...")
                jobs = scrape_jobs(
                    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
                    search_term=search_term,
                    location=city,
                    results_wanted=self.results_wanted_per_combination,
                    country_indeed=self.country_indeed,
                    description_format=self.description_format,
                    description=True
                )
                print(f"Found {len(jobs)} {search_term} jobs for {city}")
                job_data = jobs[['title', 'company', 'location', 'description']].to_dict('records')
                self.save_data(job_data, city, search_term)
                pbar.update(1)  # Update the progress bar
                print(f"progress: {pbar.n}/{pbar.total}")

    def save_data(self, job_data, city, search_term):
        jobs_df = pd.DataFrame(job_data)
        output_file = f"../data/ind_data/job_data_{city}_{search_term}.csv"
        jobs_df.to_csv(output_file, index=False)
        print(f"Job data saved to {output_file}")

    def create_dataframe(self):
        # Combine all the individual CSV files into a single DataFrame
        csv_files = [f for f in os.listdir("../data/ind_data") if f.endswith(".csv")]
        dataframes = []
        for file in csv_files:
            file_path = os.path.join("../data/ind_data", file)
            df = pd.read_csv(file_path)
            dataframes.append(df)
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df

    def save_dataframe(self, output_file):
        self.jobs_df = self.create_dataframe()  # Create the DataFrame before saving
        self.jobs_df.to_csv(output_file, index=False)
        print(f"Job data saved to {output_file}")