import streamlit as st
from src.data_loader import load_cleaned_data
from src.components import render_sidebar

st.set_page_config(page_title="Perfume dashboard", layout="wide", page_icon="assets/perfume.png")
st.title("Perfume Analytics")
df = load_cleaned_data()
filtered_df = render_sidebar(df)