from jobspy import scrape_jobs
import pandas as pd
from tqdm import tqdm

class JobScraper:
    def __init__(self, search_terms, cities, country_indeed='USA', description_format='markdown', results_wanted_per_combination=1000):
        self.search_terms = search_terms  # Updated to be plural, expecting a list of search terms (job titles)
        self.cities = cities
        self.country_indeed = country_indeed
        self.description_format = description_format
        self.results_wanted_per_combination = results_wanted_per_combination
        self.job_data = []

    def scrape_jobs(self):
        total_combinations = len(self.cities) * len(self.search_terms)
        pbar = tqdm(total=total_combinations, desc="Scraping Jobs", unit="combination", dynamic_ncols=True, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
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
                    description=True  # Include job descriptions
                )
                print(f"Found {len(jobs)} {search_term} jobs for {city}")
                self.job_data.extend(jobs[['title', 'company', 'location', 'description']].to_dict('records'))
                pbar.update(1)  # Update the progress bar
                print(f"progress: {pbar.n}/{pbar.total}")

        pbar.close()  # Close the progress bar

    def create_dataframe(self):
        self.jobs_df = pd.DataFrame(self.job_data)
        return self.jobs_df

    def save_dataframe(self, output_file):
        self.jobs_df.to_csv(output_file, index=False)
        print(f"Job data saved to {output_file}")