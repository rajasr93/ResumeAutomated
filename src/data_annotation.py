import os
import pandas as pd
import ast
import anthropic
from tqdm import tqdm
import logging
import time

class DataAnnotator:
    def __init__(self, api_key_path, sleep_time=1, output_path='annotated_data.csv', max_retries=3, initial_delay=1):
        self.api_key_path = api_key_path
        self.api_key = self.load_api_key()
        self.client = self.initialize_client()
        self.df = None
        self.sleep_time = sleep_time
        self.output_path = output_path
        self.max_retries = max_retries
        self.initial_delay = initial_delay

    def load_api_key(self):
        try:
            with open(self.api_key_path, 'r') as f:
                api_key = f.read().strip()
            return api_key
        except FileNotFoundError:
            print("API key file not found.")
            return None

    def initialize_client(self):
        if self.api_key:
            client = anthropic.Anthropic(api_key=self.api_key)
            print("Client connection successful")
            return client
        else:
            print("API key not found. Cannot initialize client.")
            return None

    def load_data(self, data):
        if isinstance(data, pd.DataFrame):
            self.df = data.copy()
            self.df = self.df.dropna()
            self.df = self.df.reset_index(drop=True)
        else:
            print("Invalid data format. Please provide a pandas DataFrame.")

    def process_description(self, description):
        if self.client:
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.0,
                system="You are an ATS system and you have to parse the following text and then you have to extract the hard skills, soft skills and key words from the text. The hard skills, soft skills and keywords should be in the form of a Python dictionary with keys being 'hard_skills', 'soft_skills' and 'key_words', and values being the Python list of all those skills, without any other information or text.",
                messages=[{"role": "user", "content": description}]
            )
            content_blocks = message.content
            if content_blocks and isinstance(content_blocks, list):
                content_block_text = content_blocks[0].text
                json_str_start = content_block_text.find('{')
                dict_str = content_block_text[json_str_start:]
                skills_dict = ast.literal_eval(dict_str)
                return skills_dict
            else:
                return {}
        else:
            print("Client not initialized. Cannot process description.")
            return {}

    def annotate_data(self):
        failed_annotations = []
        if self.df is not None:
            if os.path.exists(self.output_path):
                os.remove(self.output_path)

            total_rows = len(self.df)
            pbar = tqdm(total=total_rows, desc="Annotating Descriptions", unit="description")

            for idx, row in self.df.iterrows():
                retry_count = 0
                while retry_count < self.max_retries:
                    try:
                        result = self.process_description(row['description'])
                        time.sleep(self.sleep_time)  # Sleep after each API call

                        if isinstance(result, dict):
                            row['hard_skills'] = result.get('hard_skills', [])
                            row['soft_skills'] = result.get('soft_skills', [])
                            row['keywords'] = result.get('key_words', [])
                        else:
                            failed_annotations.append(idx)
                            row['hard_skills'] = []
                            row['soft_skills'] = []
                            row['keywords'] = []

                        # Save the annotated data point to CSV
                        row.to_frame().T.to_csv(self.output_path, mode='a', header=not os.path.exists(self.output_path), index=False)
                        break  # Break out of the retry loop if successful
                    except Exception as e:  # Using a more general Exception class
                        logging.error(f"Error annotating row {idx}: {str(e)}")
                        if "rate limit" in str(e).lower():  # Check if the error message is about rate limiting
                            retry_count += 1
                            if retry_count < self.max_retries:
                                delay = self.initial_delay * (2 ** (retry_count - 1))
                                logging.warning(f"Rate limit exceeded. Retrying in {delay} seconds...")
                                time.sleep(delay)
                            else:
                                logging.error(f"Max retries exceeded for row {idx}. Skipping annotation.")
                                failed_annotations.append(idx)
                        else:
                            failed_annotations.append(idx)
                        break  # Break out of the retry loop for other errors

                pbar.update(1)  # Update the progress bar

            pbar.close()  # Close the progress bar

            return failed_annotations
        else:
            print("Data not loaded. Cannot annotate data.")
            return failed_annotations

    def save_annotated_data(self, output_path):
        print(f"Annotated data already saved to: {self.output_path}")
    
    def save_annotated_data(self, output_path):
        if self.df is not None:
            self.df.to_csv(output_path, index=False)
            print(f"Annotated data saved to: {output_path}")
        else:
            print("Data not loaded. Cannot save annotated data.")








