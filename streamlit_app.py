import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Climate Risk Dashboard", layout="wide")
st.title("MASA Climate Risk Interactive Dashboard")
st.caption("Malaysia vs Vietnam | WDI + Disaster + Stress-Test + 2024 GHG Forecast")


@st.cache_data
def load_data():
    climate = pd.read_csv("powerbi_fact_climate_indicators.csv")
    disaster = pd.read_csv("powerbi_fact_disasters.csv")
    stress = pd.read_csv("powerbi_fact_stress_test.csv")
    ghg = pd.read_csv("ghg_2024_prediction.csv")

    country_map = {"Viet Nam": "Vietnam"}
    climate["Country"] = climate["Country"].replace(country_map)
    disaster["Country"] = disaster["Country"].replace(country_map)
    if "country" in stress.columns:
        stress["country"] = stress["country"].replace(country_map)
    if "country" in ghg.columns:
        ghg["country"] = ghg["country"].replace(country_map)

    climate["Year"] = pd.to_numeric(climate["Year"], errors="coerce")
    climate["Value"] = pd.to_numeric(climate["Value"], errors="coerce")
    disaster["Year"] = pd.to_numeric(disaster["Year"], errors="coerce")
    disaster["Deaths"] = pd.to_numeric(disaster["Deaths"], errors="coerce").fillna(0)
    disaster["Affected"] = pd.to_numeric(disaster["Affected"], errors="coerce").fillna(0)

    return climate, disaster, stress, ghg


climate_df, disaster_df, stress_df, ghg_df = load_data()

countries = sorted(climate_df["Country"].dropna().unique().tolist())
indicators = sorted(climate_df["Indicator"].dropna().unique().tolist())
default_indicator = "Total greenhouse gas emissions including LULUCF (Mt CO2e)"
if default_indicator not in indicators:
    default_indicator = indicators[0]

st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries,
)
selected_years = st.sidebar.slider(
    "Year range",
    int(climate_df["Year"].min()),
    int(climate_df["Year"].max()),
    (2010, 2019),
)
selected_indicator = st.sidebar.selectbox(
    "Primary climate indicator",
    indicators,
    index=indicators.index(default_indicator),
)

climate_filtered = climate_df[
    (climate_df["Country"].isin(selected_countries))
    & (climate_df["Year"].between(selected_years[0], selected_years[1]))
]
disaster_filtered = disaster_df[
    (disaster_df["Country"].isin(selected_countries))
    & (disaster_df["Year"].between(selected_years[0], selected_years[1]))
]

disaster_yearly = (
    disaster_filtered.groupby(["Country", "Year"], as_index=False)
    .agg(
        events=("DisasterType", "count"),
        deaths_total=("Deaths", "sum"),
        affected_total=("Affected", "sum"),
    )
    .sort_values(["Country", "Year"])
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Countries", len(selected_countries))
col2.metric("Indicators", climate_filtered["Indicator"].nunique())
col3.metric("Total disaster events", int(disaster_yearly["events"].sum()))
col4.metric("Total affected (selected years)", f"{disaster_yearly['affected_total'].sum():,.0f}")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Climate Trends", "Disaster Exposure", "Stress Test & Finance", "2024 GHG Forecast"]
)

with tab1:
    st.subheader("Climate Indicator Trend")
    trend_df = climate_filtered[climate_filtered["Indicator"] == selected_indicator].copy()
    fig_trend = px.line(
        trend_df,
        x="Year",
        y="Value",
        color="Country",
        markers=True,
        title=selected_indicator,
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Indicator Comparison Heatmap")
    heat_df = climate_filtered.pivot_table(
        index=["Country", "Year"], columns="Indicator", values="Value", aggfunc="mean"
    ).reset_index()
    # Keep top 8 indicators by available rows for readability.
    top_inds = (
        climate_filtered.groupby("Indicator")["Value"].count().sort_values(ascending=False).head(8).index
    )
    heat_show = climate_filtered[climate_filtered["Indicator"].isin(top_inds)]
    fig_heat = px.density_heatmap(
        heat_show,
        x="Year",
        y="Indicator",
        z="Value",
        facet_col="Country",
        histfunc="avg",
        title="Average indicator value by year",
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with tab2:
    st.subheader("Disaster Events and Affected Population")
    c1, c2 = st.columns(2)
    with c1:
        fig_events = px.line(
            disaster_yearly,
            x="Year",
            y="events",
            color="Country",
            markers=True,
            title="Disaster event count",
        )
        st.plotly_chart(fig_events, use_container_width=True)
    with c2:
        fig_affected = px.line(
            disaster_yearly,
            x="Year",
            y="affected_total",
            color="Country",
            markers=True,
            title="Affected population",
        )
        st.plotly_chart(fig_affected, use_container_width=True)

    st.subheader("Disaster Type Breakdown")
    disaster_type = (
        disaster_filtered.groupby(["Country", "DisasterType"], as_index=False)["Affected"].sum()
    )
    fig_type = px.bar(
        disaster_type,
        x="DisasterType",
        y="Affected",
        color="Country",
        barmode="group",
        title="Total affected by disaster type",
    )
    st.plotly_chart(fig_type, use_container_width=True)

with tab3:
    st.subheader("2030 Stress Test")
    if "country" in stress_df.columns:
        stress_show = stress_df[stress_df["country"].isin(selected_countries)].copy()
    else:
        stress_show = stress_df.copy()

    stress_long = stress_show.melt(
        id_vars=[c for c in ["country", "year", "Scenario"] if c in stress_show.columns],
        value_vars=[c for c in ["baseline_damage_kusd_2030", "stressed_damage_kusd_2030"] if c in stress_show.columns],
        var_name="DamageType",
        value_name="DamageKUSD",
    )
    fig_stress = px.bar(
        stress_long,
        x="country",
        y="DamageKUSD",
        color="DamageType",
        barmode="group",
        title="Baseline vs stressed damage (2030)",
    )
    st.plotly_chart(fig_stress, use_container_width=True)

    st.markdown(
        "Use this view as report appendix evidence for **financial impact assessment** and **stress scenario justification**."
    )

with tab4:
    st.subheader("2024 GHG Prediction Results")
    ghg_show = ghg_df[ghg_df["country"].isin(selected_countries)].copy()
    st.dataframe(ghg_show, use_container_width=True)

    fig_ghg = px.bar(
        ghg_show,
        x="country",
        y="predicted_2024",
        color="country",
        title="Predicted 2024 GHG emissions (Mt CO2e)",
    )
    st.plotly_chart(fig_ghg, use_container_width=True)

    metric_cols = st.columns(2)
    with metric_cols[0]:
        st.metric("Average RMSE", f"{ghg_show['fit_rmse'].mean():.2f}")
    with metric_cols[1]:
        st.metric("Average R2", f"{ghg_show['fit_r2'].mean():.3f}")


st.markdown("---")
st.subheader("Download Filtered Data")
st.download_button(
    "Download filtered climate data (CSV)",
    climate_filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_climate_data.csv",
    mime="text/csv",
)
st.download_button(
    "Download yearly disaster summary (CSV)",
    disaster_yearly.to_csv(index=False).encode("utf-8"),
    file_name="yearly_disaster_summary.csv",
    mime="text/csv",
)
