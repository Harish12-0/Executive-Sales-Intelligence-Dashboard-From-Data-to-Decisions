from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Sales Data Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
DEFAULT_DATA = ROOT / "data" / "sales_demo.csv"

NAVY = "#18345D"
BLUE = "#3D8FE8"
LIGHT_BLUE = "#A9D2F5"
TAN = "#C79A6B"
PALE = "#D6E7F7"

st.markdown(
    """
    <style>
      .stApp { background: #F5FAFE; }
      [data-testid="stMetric"] {
        background: white; padding: 16px 18px; border-radius: 14px;
        border: 1px solid #DCEAF7; box-shadow: 0 2px 8px rgba(24,52,93,.06);
      }
      [data-testid="stMetricLabel"] { color: #263E60; }
      [data-testid="stMetricValue"] { color: #18345D; }
      div[data-testid="stDataFrame"] { border: 1px solid #DCEAF7; border-radius: 10px; }
      h1, h2, h3 { color: #18345D; }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv(DEFAULT_DATA)

    # Standardize column names and validate required fields.
    data.columns = [str(c).strip() for c in data.columns]
    required = {
        "Order Date", "Region", "State", "Segment", "Ship Mode",
        "Gross Sales", "Profit Margin", "COGS", "Net", "Profit"
    }
    missing = required - set(data.columns)
    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(sorted(missing))
        )

    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    for col in ["Gross Sales", "Profit Margin", "COGS", "Net", "Profit"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.dropna(subset=["Order Date", "Region", "State", "Segment"])
    data["Year"] = data["Order Date"].dt.year
    data["Month Start"] = data["Order Date"].dt.to_period("M").dt.to_timestamp()
    return data

st.title("📊 Sales Data Analysis")
st.caption("Overview · Interactive sales, profitability, and regional performance")

with st.sidebar:
    st.header("Dashboard controls")
    uploaded = st.file_uploader("Upload your sales CSV", type=["csv"])
    try:
        raw = load_data(uploaded)
    except Exception as exc:
        st.error(f"Could not load the file: {exc}")
        st.stop()

    min_year = int(raw["Year"].min())
    max_year = int(raw["Year"].max())
    selected_years = st.slider(
        "Order year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    all_regions = sorted(raw["Region"].dropna().unique().tolist())
    selected_regions = st.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
    )
    all_segments = sorted(raw["Segment"].dropna().unique().tolist())
    selected_segments = st.multiselect(
        "Segment",
        options=all_segments,
        default=all_segments,
    )

filtered = raw[
    raw["Year"].between(selected_years[0], selected_years[1])
    & raw["Region"].isin(selected_regions)
    & raw["Segment"].isin(selected_segments)
].copy()

if filtered.empty:
    st.warning("No rows match the selected filters. Change the filters to continue.")
    st.stop()

# KPI calculations
net_total = filtered["Net"].sum()
gross_total = filtered["Gross Sales"].sum()
cogs_total = filtered["COGS"].sum()
profit_total = filtered["Profit"].sum()
margin = (profit_total / gross_total * 100) if gross_total else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Net Sales", f"{net_total:,.0f}")
k2.metric("Profit Margin", f"{margin:.2f}%")
k3.metric("Profit", f"{profit_total:,.0f}")
k4.metric("COGS", f"{cogs_total:,.0f}")
k5.metric("Gross Sales", f"{gross_total:,.0f}")

st.divider()

left, center, right = st.columns([1.1, 1.5, 0.85], gap="medium")

with left:
    st.subheader("Net Sales by Segment")
    segment = (
        filtered.groupby("Segment", as_index=False)["Net"]
        .sum().sort_values("Net", ascending=False)
    )
    fig_segment = px.bar(
        segment, x="Segment", y="Net", color="Segment",
        color_discrete_sequence=[TAN, BLUE, PALE],
        labels={"Net": "Net Sales", "Segment": ""},
    )
    fig_segment.update_layout(
        showlegend=False, margin=dict(l=8, r=8, t=10, b=8),
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis_title="", xaxis_title="",
    )
    st.plotly_chart(fig_segment, use_container_width=True)

with center:
    st.subheader("Net Sales and Profit by Month")
    monthly = (
        filtered.groupby("Month Start", as_index=False)[["Net", "Profit"]]
        .sum().sort_values("Month Start")
    )
    fig_month = go.Figure()
    fig_month.add_trace(go.Scatter(
        x=monthly["Month Start"], y=monthly["Net"], name="Net Sales",
        mode="lines", line=dict(color=NAVY, width=2.5),
        fill="tozeroy", fillcolor="rgba(24,52,93,0.16)"
    ))
    fig_month.add_trace(go.Scatter(
        x=monthly["Month Start"], y=monthly["Profit"], name="Profit",
        mode="lines", line=dict(color=TAN, width=2.5),
        fill="tozeroy", fillcolor="rgba(199,154,107,0.25)"
    ))
    fig_month.update_layout(
        margin=dict(l=8, r=8, t=10, b=8),
        plot_bgcolor="white", paper_bgcolor="white",
        legend=dict(orientation="h", y=1.12, x=0),
        xaxis_title="", yaxis_title="Amount",
    )
    st.plotly_chart(fig_month, use_container_width=True)

with right:
    st.subheader("Net Sales by Region")
    region = filtered.groupby("Region", as_index=False)["Net"].sum()
    fig_region = px.pie(
        region, names="Region", values="Net", hole=0.58,
        color_discrete_sequence=[NAVY, TAN, BLUE, PALE],
    )
    fig_region.update_traces(
        textposition="outside", textinfo="percent",
        hovertemplate="%{label}<br>Net: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
    )
    fig_region.update_layout(
        margin=dict(l=4, r=4, t=10, b=4),
        showlegend=True, legend=dict(orientation="h", y=-0.12),
        paper_bgcolor="white",
    )
    st.plotly_chart(fig_region, use_container_width=True)

bottom_left, bottom_right = st.columns([2.1, 1], gap="medium")
with bottom_left:
    st.subheader("Sales Detail")
    detail_cols = [
        "Region", "State", "Ship Mode", "Gross Sales",
        "Profit Margin", "COGS", "Net", "Profit"
    ]
    detail = filtered[detail_cols].sort_values("Net", ascending=False)
    st.dataframe(
        detail.style.format({
            "Gross Sales": "{:,.2f}", "Profit Margin": "{:.2f}%",
            "COGS": "{:,.2f}", "Net": "{:,.2f}", "Profit": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True,
        height=350,
    )
    st.download_button(
        "Download filtered data as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )

with bottom_right:
    st.subheader("Net Sales by State")
    state = (
        filtered.groupby("State", as_index=False)["Net"]
        .sum().sort_values("Net", ascending=False).head(8)
    )
    fig_state = px.bar(
        state.sort_values("Net"), x="Net", y="State", orientation="h",
        color="Net", color_continuous_scale=[PALE, BLUE, NAVY],
        labels={"Net": "Net Sales", "State": ""},
    )
    fig_state.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=8, b=8),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="", yaxis_title="",
    )
    st.plotly_chart(fig_state, use_container_width=True)

st.caption(
    "Note: The included CSV is synthetic demo data created for this repository. "
    "Replace it with your authorized dataset before using the dashboard for business decisions."
)
