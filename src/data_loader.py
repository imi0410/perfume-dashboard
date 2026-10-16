import pandas as pd
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / 'data' / 'raw' / 'fragrance.csv'
CLEANED_PATH = BASE_DIR / 'data' / 'cleaned'

def load_data(path: Path = RAW_PATH):
    df = pd.read_csv(path, sep=';', encoding='latin1', on_bad_lines='skip')
    return df

def dataset_properties(df: pd.DataFrame):
    print(df.shape)
    print(df.isnull().sum())
    print(df.dtypes)

def clean_data(df: pd.DataFrame):
    cleaned_df = df.copy()
    # changing the name of the columns
    cleaned_df.columns = (
        cleaned_df.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    #converting rating_value to float
    cleaned_df["rating_value"] = (
        cleaned_df["rating_value"].astype(str).str.replace(",", ".").str.strip()
    )
    cleaned_df["rating_value"] = pd.to_numeric(
        cleaned_df["rating_value"], errors="coerce"
    )
    #converting to int and remove perfumes below year 1980
    cleaned_df["year"] = pd.to_numeric(cleaned_df["year"], errors="coerce")
    cleaned_df = cleaned_df[cleaned_df["year"] >= 1980]
    cleaned_df["year"] = cleaned_df["year"].astype(int)
    #converting to int from float
    cleaned_df["rating_count"] = cleaned_df["rating_count"].astype(int)
    #droping duplicated rows
    cleaned_df = cleaned_df.drop_duplicates()
    #filling nulls with None
    accord_cols = ["mainaccord1", "mainaccord2", "mainaccord3", "mainaccord4", "mainaccord5"]
    cleaned_df[accord_cols] = cleaned_df[accord_cols].fillna("None")
    return cleaned_df

def export_cleaned_data(df: pd.DataFrame, path: str = CLEANED_PATH):
    cleaned_df = df.copy()
    cleaned_df.to_csv(CLEANED_PATH / "fragrance_cleaned.csv", index=False)

@st.cache_data
def load_cleaned_data(path: Path = CLEANED_PATH / "fragrance_cleaned.csv"):
    return pd.read_csv(path)

if __name__ == '__main__':
    export_cleaned_data(clean_data(load_data(RAW_PATH)))
    dataset_properties(clean_data(load_data(RAW_PATH)))