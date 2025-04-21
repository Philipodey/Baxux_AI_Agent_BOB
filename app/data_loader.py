import pandas as pd

def load_bottle_data(path="data/bottles.csv"):
    df = pd.read_csv(path)
    print("BOTTLE DATA COLUMNS:", df.columns)
    return df



import json

def load_user_bar(path="tests/sample_bars.json"):
    with open(path) as f:
        return json.load(f)
