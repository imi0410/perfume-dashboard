import pandas as pd
import streamlit as st

def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.title("Filter panel")

    #year filter
    min_y, max_y = int(df["year"].min()), int(df["year"].max())
    selected_years = st.sidebar.slider("Release year", min_y, max_y,(2000,max_y))

    #minimum score filter
    min_rating = st.sidebar.slider("Minimal rating", 1.0,5.0,3.5,0.1)

    #target audience filter
    genders = df["gender"].dropna().unique().tolist()
    selected_genders = st.sidebar.multiselect(
        "Target audience (gender)", genders, default=genders
    )

    #top accords filter
    top_accords = df["mainaccord1"].value_counts().head(12).index.tolist()
    selected_accords = st.sidebar.multiselect(
        "Top accords", top_accords, default=top_accords[:6]
    )

    #márkakereső
    brand_search = st.sidebar.text_input("Brand searching", "")

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
