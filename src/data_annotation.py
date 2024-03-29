import pandas as pd
import json
import anthropic

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
            self.df = data.dropna().reset_index(drop=True)
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
                try:
                    json_str_start = content_block_text.find('{')
                    dict_str = content_block_text[json_str_start:]
                    skills_dict = json.loads(dict_str)
                    return skills_dict
                except json.JSONDecodeError:
                    print(f"Failed to parse response: {content_block_text}")
                    return {}
            else:
                return {}
        else:
            print("Client not initialized. Cannot process description.")
            return {}

if __name__ == "__main__":
    api_key_path = 'api-key.txt'
    annotator = DataAnnotator(api_key_path)
    description = "We are looking for a software engineer with experience in Python, Java, and SQL. The ideal candidate should have strong problem-solving skills and be a team player."
    skills = annotator.process_description(description)
    print(skills)








