import os
import pandas as pd
import ast
import anthropic
from tqdm import tqdm

class DataAnnotator:
    def __init__(self, api_key_path):
        self.api_key_path = api_key_path
        self.api_key = self.load_api_key()
        self.client = self.initialize_client()
        self.df = None

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
            annotation = []
            total_rows = len(self.df)
            pbar = tqdm(total=total_rows, desc="Annotating Descriptions", unit="description")

            for idx, row in self.df.iterrows():
                try:
                    result = self.process_description(row['description'])
                    if isinstance(result, dict):
                        annotation.append(result)
                    else:
                        failed_annotations.append(idx)
                        annotation.append({})
                except Exception as e:
                    print(f"Error annotating row {idx}: {e}")
                    failed_annotations.append(idx)
                    annotation.append({})
                pbar.update(1)  # Update the progress bar

            pbar.close()  # Close the progress bar

            if annotation:
                self.df['hard_skills'] = [x.get('hard_skills', []) for x in annotation]
                self.df['soft_skills'] = [x.get('soft_skills', []) for x in annotation]
                self.df['keywords'] = [x.get('key_words', []) for x in annotation]
            else:
                print("No annotations could be generated.")

            return self.df, failed_annotations
        else:
            print("Data not loaded. Cannot annotate data.")
            return None, failed_annotations
    
    def save_annotated_data(self, output_path):
        if self.df is not None:
            self.df.to_csv(output_path, index=False)
            print(f"Annotated data saved to: {output_path}")
        else:
            print("Data not loaded. Cannot save annotated data.")








