import pandas as pd

df = pd.read_csv(r"tweet_dialect_dataset.csv", lineterminator='\n')
for row in df.iterrows():
    print(row[0])
    print(row[1])