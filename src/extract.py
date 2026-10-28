import pandas as pd
from pathlib import Path


def extract_data(file_path):

    df = pd.read_csv(file_path)

    return df