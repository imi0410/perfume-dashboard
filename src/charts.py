import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"
TEXT_COLOR = "#2b1f1d"
GRID_COLOR = "rgba(180, 160, 160, 0.35)"
FIXED_ACCORDS = [
    "citrus",
    "woody",
    "floral",
    "fruity",
    "aromatic",
    "white floral",
    "warm spicy",
]


def create_radar_chart(df: pd.DataFrame) -> go.Figure:
  crosstab_res = pd.crosstab(
      df["gender"], df["mainaccord1"], normalize="index"
  )
  crosstab_res = crosstab_res.reindex(columns=FIXED_ACCORDS, fill_value=0)

  fig = go.Figure()

  palette = {
      "women": "#e05a5a",
      "men": "#1e88e5",
      "unisex": "#43a047",
  }

  for g in ["women", "men", "unisex"]:
    if g in crosstab_res.index:
      vals = crosstab_res.loc[g, FIXED_ACCORDS].tolist()
      vals.append(vals[0])
      theta_labels = [c.title() for c in FIXED_ACCORDS] + [
          FIXED_ACCORDS[0].title()
      ]

      color = palette.get(g, "#555555")

      fig.add_trace(
          go.Scatterpolar(
              r=vals,
              theta=theta_labels,
              name=g.capitalize(),
              mode="lines+markers",
              line=dict(color=color, width=2),
              marker=dict(size=4, color=color),
          )
      )

  fig.update_layout(
      title=dict(
          text="Scent Profile for Target Audience",
          font=dict(size=16, color=TEXT_COLOR, family="sans-serif"),
      ),
      polar=dict(
          radialaxis=dict(
              visible=True,
              range=[0, 0.22],
              showticklabels=False,
              showline=False,
              gridcolor="rgba(180, 180, 180, 0.4)",
              gridwidth=0.8,
          ),
          angularaxis=dict(
              direction="clockwise",
              rotation=90,
              showline=True,
              linecolor="rgba(160, 160, 160, 0.6)",
              gridcolor="rgba(180, 180, 180, 0.4)",
              gridwidth=0.8,
              tickfont=dict(color=TEXT_COLOR, size=11, family="sans-serif"),
          ),
          bgcolor="rgba(0, 0, 0, 0)",
      ),
      paper_bgcolor=PAPER_BG,
      font=dict(color=TEXT_COLOR),
      margin=dict(l=35, r=35, t=45, b=35),
      legend=dict(
          orientation="h",
          yanchor="bottom",
          y=-0.22,
          xanchor="center",
          x=0.5,
          font=dict(color=TEXT_COLOR, size=12),
      ),
      height=380,
  )
  return fig


def create_heatmap(df: pd.DataFrame) -> go.Figure:
  top_accs = df["mainaccord1"].value_counts().head(6).index.tolist()
  sub_df = df[
      df["mainaccord1"].isin(top_accs)
      & df["mainaccord2"].isin(top_accs)
      & (df["mainaccord2"] != "None")
  ]

  if sub_df.empty:
    return go.Figure()

  matrix = pd.crosstab(sub_df["mainaccord1"], sub_df["mainaccord2"]).reindex(
      index=top_accs, columns=top_accs, fill_value=0
  )
  sym_matrix = matrix + matrix.T
  sym_vals = sym_matrix.to_numpy(copy=True)
  np.fill_diagonal(sym_vals, 0)

  fig = px.imshow(
      sym_vals,
      labels=dict(
          x="Secondary accord", y="Main accord", color="Number of perfumes"
      ),
      x=[x.title() for x in sym_matrix.columns],
      y=[y.title() for y in sym_matrix.index],
      color_continuous_scale=[
          [0.0, "#f9f6f5"],
          [0.3, "#e5cfc9"],
          [0.7, "#ba7a82"],
          [1.0, "#60373d"],
      ],
      text_auto=True,
  )
  fig.update_layout(
      title=dict(
          text="Scent Accord Combinations",
          font=dict(size=16, color=TEXT_COLOR),
      ),
      paper_bgcolor=PAPER_BG,
      plot_bgcolor=PLOT_BG,
      font=dict(color=TEXT_COLOR),
      xaxis=dict(
          tickfont=dict(color=TEXT_COLOR, size=11),
          title=dict(
              text="Secondary accord",
              font=dict(color=TEXT_COLOR, size=12),
          ),
      ),
      yaxis=dict(
          tickfont=dict(color=TEXT_COLOR, size=11),
          title=dict(
              text="Main accord",
              font=dict(color=TEXT_COLOR, size=12),
          ),
      ),
      coloraxis_colorbar=dict(
          title=dict(
              text="Number of perfumes",
              font=dict(color=TEXT_COLOR, size=11),
          ),
          tickfont=dict(color=TEXT_COLOR, size=10),
      ),
      margin=dict(l=35, r=35, t=45, b=45),
      height=380,
  )
  return fig


def create_area_chart(df: pd.DataFrame) -> go.Figure:
  yearly = (
      df.groupby(["year", "mainaccord1"]).size().reset_index(name="count")
  )
  fig = px.area(
      yearly,
      x="year",
      y="count",
      color="mainaccord1",
      labels={
          "year": "Release date",
          "count": "Number of perfumes",
          "mainaccord1": "Accord",
      },
      color_discrete_sequence=[
          "#b26871",
          "#2b5c8f",
          "#d4883b",
          "#8c7284",
          "#5e454b",
          "#8090a2",
      ],
  )
  fig.update_layout(
      title=dict(
          text="Evolution of Fragrance Trends Over Time",
          font=dict(size=16, color=TEXT_COLOR),
      ),
      paper_bgcolor=PAPER_BG,
      plot_bgcolor=PLOT_BG,
      font=dict(color=TEXT_COLOR),
      xaxis=dict(
          gridcolor=GRID_COLOR,
          tickfont=dict(color=TEXT_COLOR, size=11),
          title=dict(
              text="Release date",
              font=dict(color=TEXT_COLOR, size=12),
          ),
      ),
      yaxis=dict(
          gridcolor=GRID_COLOR,
          tickfont=dict(color=TEXT_COLOR, size=11),
          title=dict(
              text="Number of perfumes",
              font=dict(color=TEXT_COLOR, size=12),
          ),
      ),
      margin=dict(l=35, r=35, t=45, b=45),
      legend=dict(
          orientation="h",
          yanchor="bottom",
          y=-0.35,
          xanchor="center",
          x=0.5,
          title=dict(font=dict(color=TEXT_COLOR, size=12)),
          font=dict(color=TEXT_COLOR, size=11),
      ),
      height=380,
  )
  return fig


def create_scatter_plot(df: pd.DataFrame) -> go.Figure:
    brand_stats = (
        df.groupby("brand")
        .agg(
            count=("perfume", "count"),
            avg_rating=("rating_value", "mean"),
            rating_count=("rating_count", "sum"),
        )
        .reset_index()
    )

    brand_filtered = brand_stats[
        (brand_stats["count"] >= 3) & (brand_stats["rating_count"] >= 30)
    ].copy()

    brand_filtered["avg_rating_rounded"] = brand_filtered["avg_rating"].round(2)

    fig = px.scatter(
        brand_filtered,
        x="count",
        y="avg_rating",
        size="rating_count",
        color="avg_rating",
        hover_name="brand",
        log_x=True,
        labels={
            "count": "Number of released perfumes",
            "avg_rating": "Average rating",
            "rating_count": "Total ratings",
        },
        color_continuous_scale=[
            [0.0, "#d8b4a0"],
            [0.5, "#b26871"],
            [1.0, "#4a1c24"],
        ],
        size_max=32,
        opacity=0.75,
    )

    fig.update_traces(
        marker=dict(line=dict(width=0.8, color="#ffffff")),
        hovertemplate=(
            "<b>%{hovertext}</b><br><br>"
            "Perfumes released: %{x}<br>"
            "Average rating: %{y:.2f} / 5.0<br>"
            "Total ratings: %{marker.size:,}<br>"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        title=dict(
            text="Positioning of brands",
            font=dict(size=16, color=TEXT_COLOR),
        ),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_COLOR),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            tickfont=dict(color=TEXT_COLOR, size=11),
            title=dict(
                text="Number of released perfumes (log scale)",
                font=dict(color=TEXT_COLOR, size=12),
            ),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            tickfont=dict(color=TEXT_COLOR, size=11),
            title=dict(
                text="Average rating",
                font=dict(color=TEXT_COLOR, size=12),
            ),
        ),
        coloraxis_colorbar=dict(
            title=dict(
                text="Average rating",
                font=dict(color=TEXT_COLOR, size=11),
            ),
            tickfont=dict(color=TEXT_COLOR, size=10),
        ),
        margin=dict(l=35, r=35, t=45, b=35),
        height=380,
    )
    return fig