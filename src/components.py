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

def render_kpis(df: pd.DataFrame):
  k1, k2, k3, k4 = st.columns(4)

  with k1:
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Filtered perfumes</div>
            <div class="metric-value" style="color: #38bdf8;">{len(df):,}</div>
        </div>""",
        unsafe_allow_html=True,
    )

  with k2:
    mean_val = df["rating_value"].mean() if not df.empty else 0
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Average rating</div>
            <div class="metric-value" style="color: #fbbf24;">{mean_val:.2f} / 5.0</div>
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
            <div class="metric-value" style="color: #ff4b72;">{top_acc}</div>
        </div>""",
        unsafe_allow_html=True,
    )

  with k4:
    votes = df["rating_count"].sum() if not df.empty else 0
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-label">Rating count</div>
            <div class="metric-value" style="color: #a78bfa;">{votes:,}</div>
        </div>""",
        unsafe_allow_html=True,
    )