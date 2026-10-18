import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PLOT_BG = "#1a1d29"
PAPER_BG = "#0f111a"
TEXT_COLOR = "#f8fafc"
GRID_COLOR = "#2d3248"


def create_radar_chart(df: pd.DataFrame) -> go.Figure:
  top_accords = df["mainaccord1"].value_counts().head(7).index.tolist()
  if len(top_accords) < 3:
    return go.Figure()

  crosstab_res = pd.crosstab(
      df["gender"], df["mainaccord1"], normalize="index"
  )
  radar_cols = [c for c in top_accords if c in crosstab_res.columns]

  fig = go.Figure()
  palette = {"women": "#ff4b72", "men": "#38bdf8", "unisex": "#34d399"}

  for g in df["gender"].unique():
    if g in crosstab_res.index:
      vals = crosstab_res.loc[g, radar_cols].tolist()
      vals.append(vals[0])
      theta_labels = [c.title() for c in radar_cols] + [radar_cols[0].title()]

      fig.add_trace(
          go.Scatterpolar(
              r=vals,
              theta=theta_labels,
              fill="toself",
              name=g.capitalize(),
              line=dict(color=palette.get(g, "#cbd5e1"), width=2),
              opacity=0.35,
          )
      )

  fig.update_layout(
      title=dict(
          text="Scent Profile for Target Audience",
          font=dict(size=15, color=TEXT_COLOR),
      ),
      polar=dict(
          radialaxis=dict(
              visible=True, showticklabels=False, gridcolor=GRID_COLOR
          ),
          angularaxis=dict(gridcolor=GRID_COLOR),
          bgcolor=PLOT_BG,
      ),
      paper_bgcolor=PAPER_BG,
      font=dict(color=TEXT_COLOR),
      margin=dict(l=30, r=30, t=40, b=30),
      legend=dict(
          orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5
      ),
      height=380,
  )
  return fig


def create_heatmap(df: pd.DataFrame) -> go.Figure:
  top_accs = df["mainaccord1"].value_counts().head(8).index.tolist()
  sub_df = df[
      df["mainaccord1"].isin(top_accs)
      & df["mainaccord2"].isin(top_accs)
      & (df["mainaccord2"] != "None")
  ]

  if sub_df.empty:
    return go.Figure()

  matrix = pd.crosstab(sub_df["mainaccord1"], sub_df["mainaccord2"])
  fig = px.imshow(
      matrix,
      labels=dict(
          x="Secondary accord", y="Main accord", color="Number of perfumes"
      ),
      x=[x.title() for x in matrix.columns],
      y=[y.title() for y in matrix.index],
      color_continuous_scale="Viridis",
      text_auto=True,
  )
  fig.update_layout(
      title=dict(
          text="Scent Accord Combinations",
          font=dict(size=15, color=TEXT_COLOR),
      ),
      paper_bgcolor=PAPER_BG,
      plot_bgcolor=PLOT_BG,
      font=dict(color=TEXT_COLOR),
      margin=dict(l=30, r=30, t=40, b=30),
      height=380,
  )
  return fig

def create_area_chart(df: pd.DataFrame) -> go.Figure:
  yearly = (
      df.groupby(["year", "mainaccord1"]).size().reset_index(name="db")
  )
  fig = px.area(
      yearly,
      x="year",
      y="db",
      color="mainaccord1",
      labels={
          "year": "Release date",
          "darab": "Number of perfumes",
          "mainaccord1": "",
      },
      color_discrete_sequence=px.colors.qualitative.Safe,
  )
  fig.update_layout(
      title=dict(
          text="Evolution of Fragrance Trends Over Time",
          font=dict(size=15, color=TEXT_COLOR),
      ),
      paper_bgcolor=PAPER_BG,
      plot_bgcolor=PLOT_BG,
      font=dict(color=TEXT_COLOR),
      xaxis=dict(gridcolor=GRID_COLOR),
      yaxis=dict(gridcolor=GRID_COLOR),
      margin=dict(l=30, r=30, t=40, b=30),
      legend=dict(
          orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5
      ),
      height=380,
  )
  return fig