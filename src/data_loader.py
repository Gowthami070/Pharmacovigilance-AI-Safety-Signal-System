import pandas as pd


def load_data(file_path):
    """
    Load the safety dataset from an Excel file.
    """
    df = pd.read_excel(file_path)
    return df