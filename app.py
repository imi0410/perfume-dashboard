import streamlit as st
from src.data_loader import load_cleaned_data
from src.components import render_sidebar, render_kpis
from src.charts import create_radar_chart

st.set_page_config(page_title="Perfume dashboard", layout="wide", page_icon="assets/perfume.png")
st.title("Perfume Analytics")

st.markdown(
    """
<style>
    .metric-card {
        background-color: #1a1d29;
        border: 1px solid #2d3248;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
    }
    .metric-label { font-size: 0.8rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; }
    .metric-value { font-size: 1.6rem; font-weight: 800; margin-top: 4px; }
</style>
""",
    unsafe_allow_html=True,
)

df = load_cleaned_data()
filtered_df = render_sidebar(df)
render_kpis(filtered_df)

c1, c2 = st.columns(2)
with c1:
  st.plotly_chart(create_radar_chart(filtered_df), use_container_width=True)