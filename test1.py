import os
import pandas as pd

files = [f for f in os.listdir('finalized_data')]
dfs = [pd.read_csv(os.path.join('finalized_data', f)) for f in files]
