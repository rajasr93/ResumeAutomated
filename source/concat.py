import pandas as pd
import os

# from the data folder, reading all the files starting with jobs:
files = [f for f in os.listdir('../data') if f.startswith('jobs')]
# reading all the files into a list of dataframes
dfs = [pd.read_csv(os.path.join('../data', f)) for f in files]
# # concatenating all the dataframes into one
df = pd.concat(dfs)
print(df.shape)

# only need to keep title, company, location and description columns
df = df[['title', 'company', 'location', 'description']]

df.to_csv('../finalized_data/financial_analyst_job.csv', index=False)