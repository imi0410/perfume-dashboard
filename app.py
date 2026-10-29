import streamlit as st
from src.charts import (
    create_area_chart,
    create_heatmap,
    create_radar_chart,
    create_scatter_plot,
)
from src.components import render_kpis, render_sidebar, set_background
from src.data_loader import load_cleaned_data

st.set_page_config(
    page_title="Perfume dashboard", layout="wide", page_icon="assets/perfume.png"
)
set_background("assets/wallpaper.jpg")
st.markdown(
    """
<style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #fcfbfa !important;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid rgba(220, 205, 202, 0.7);
        border-radius: 12px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(60, 40, 40, 0.05);
    }
    .metric-label {
        font-size: 0.78rem;
        color: #7d6b68;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #2b1f1d !important;
    }
    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid rgba(220, 205, 202, 0.7);
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(60, 40, 40, 0.05);
    }
    h1 {
        color: #2b1f1d !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] [data-testid="stHeading"] h1 {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] [data-baseweb="tag"] span,
section[data-testid="stSidebar"] [data-baseweb="tag"] div,
section[data-testid="stSidebar"] [data-baseweb="tag"] svg,
section[data-testid="stSidebar"] [data-baseweb="tag"] * {
    color: #000000 !important;
    fill: #000000 !important;
    stroke: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span,
[data-testid="stSidebar"] [data-baseweb="tag"] div,
[data-testid="stSidebar"] span[data-baseweb="tag"] span,
section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

[data-testid="stSidebar"] [data-baseweb="tag"] svg,
[data-testid="stSidebar"] [data-baseweb="tag"] svg path,
section[data-testid="stSidebar"] [data-baseweb="tag"] svg * {
    fill: #000000 !important;
    stroke: #000000 !important;
    color: #000000 !important;
}
header[data-testid="stHeader"] {
    background-color: transparent !important;
    background: transparent !important;
}
#perfume-analytics{
    padding-top: 0;
    margin-top:0;
}
</style>
""",
    unsafe_allow_html=True,
)
st.title("Perfume Analytics")

df = load_cleaned_data()
filtered_df = render_sidebar(df)
if filtered_df.empty:
    st.warning("...🚫 🛑 ⚠️...")
    st.stop()
render_kpis(filtered_df)

st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
  st.plotly_chart(create_radar_chart(filtered_df), use_container_width=True)
with c2:
  st.plotly_chart(create_heatmap(filtered_df), use_container_width=True)

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
  st.plotly_chart(create_area_chart(filtered_df), use_container_width=True)
with c4:
  st.plotly_chart(create_scatter_plot(filtered_df), use_container_width=True)