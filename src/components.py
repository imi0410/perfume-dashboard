import base64
from pathlib import Path
import pandas as pd
import streamlit as st
import os


def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
  st.sidebar.title("Filter panel")

  min_y, max_y = int(df["year"].min()), int(df["year"].max())
  selected_years = st.sidebar.slider(
      "Release year", min_y, max_y, (2000, max_y)
  )

  min_rating = st.sidebar.slider("Minimal rating", 1.0, 5.0, 3.5, 0.1)

  genders = df["gender"].dropna().unique().tolist()
  selected_genders = st.sidebar.multiselect(
      "Target audience (gender)", genders, default=genders
  )

  accords = df["mainaccord1"].value_counts().index.tolist()
  selected_accords = st.sidebar.multiselect(
      "Main accords", accords, default=accords[:6]
  )

  brand_search = st.sidebar.text_input("Brand search", "")

  filtered = df[
      (df["year"] >= selected_years[0])
      & (df["year"] <= selected_years[1])
      & (df["rating_value"] >= min_rating)
      & (df["gender"].isin(selected_genders))
      & (df["mainaccord1"].isin(selected_accords))
  ]

  if brand_search.strip():
    filtered = filtered[
        filtered["brand"].str.contains(
            brand_search.strip(), case=False, na=False
        )
    ]

  return filtered


def render_kpis(df: pd.DataFrame):
  k1, k2, k3, k4 = st.columns(4)

  with k1:
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Filtered perfumes</div>
            <div class="metric-value">{len(df):,}</div>
        </div>""",
        unsafe_allow_html=True,
    )

  with k2:
    mean_val = df["rating_value"].mean() if not df.empty else 0
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Average rating</div>
            <div class="metric-value">{mean_val:.2f} / 5.0</div>
        </div>""",
        unsafe_allow_html=True,
    )

  with k3:
    top_acc = (
        df["mainaccord1"].value_counts().index[0].title()
        if not df.empty
        else "-"
    )
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Dominant accord</div>
            <div class="metric-value">{top_acc}</div>
        </div>""",
        unsafe_allow_html=True,
    )

  with k4:
    votes = df["rating_count"].sum() if not df.empty else 0
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Rating count</div>
            <div class="metric-value">{votes:,}</div>
        </div>""",
        unsafe_allow_html=True,
    )

def set_background(image_path: str):
    if not os.path.exists(image_path):
        return

    ext = image_path.split(".")[-1].lower()
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp,
        div[data-testid="stAppViewContainer"],
        .stAppViewContainer,
        section.main {{
            background-image: url("data:{mime};base64,{encoded_string}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        div[data-testid="stAppViewContainer"] > .main {{
            background-color: transparent !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )