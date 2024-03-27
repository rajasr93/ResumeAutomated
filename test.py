import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# from the data folder, reading all the files starting with jobs:
files = [f for f in os.listdir('data') if f.startswith('jobs')]
# reading all the files into a list of dataframes
dfs = [pd.read_csv(os.path.join('data', f)) for f in files]
# concatenating all the dataframes into one
df = pd.concat(dfs)
print(df.shape)

df.to_csv('data/finalized_data/data_analyst_jobs.csv', index=False)