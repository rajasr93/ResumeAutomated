import os
import pandas as pd
import ast
import anthropic

api_key_path = os.path.join(os.path.dirname(__file__), 'api-key.txt')
api_key = open(api_key_path).read().strip()

client = anthropic.Anthropic(api_key=api_key)
print("client connection successful")

df = pd.read_csv('../finalized_data/concatenated_data.csv')
df = df.dropna()
df = df.reset_index(drop=True)

def process_description(description):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.0,
        system="You are an ATS system and you have to parse the following text and then you have to extract the hard skills, soft skills and key words from the text. The hard skills, soft skills and keywords should be in the form of a Python dictionary with keys being 'hard_skills', 'soft_skills' and 'key_words', and values being the Python list of all those skills, without any other information or text.",
        messages=[
            {"role": "user", "content": description}
        ]
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

df['hard_skills'] = df['description'].apply(process_description).apply(lambda x: x.get('hard_skills', []))
df['soft_skills'] = df['description'].apply(process_description).apply(lambda x: x.get('soft_skills', []))
df['key_words'] = df['description'].apply(process_description).apply(lambda x: x.get('key_words', []))

print(df.head())









