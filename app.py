import streamlit as st
import pyodbc
import os
import pandas as pd
import altair as alt
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# page setup
st.set_page_config(page_title="Derbyshire Police Data Explorer", layout="wide", menu_items={
    "About": "This app allows you to explore Derbyshire Police data. You can filter the data by various criteria and visualise it using charts and maps."
})
st.title("Derbyshire Police Data Explorer", text_alignment="center")
st.caption("Explore Derbyshire open police data")
#st.markdown()

# credentials
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER", "police-sql-server.database.windows.net")   
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE", "police_data_db")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME", "rectangle")        
AZURE_SQL_PASSWORD =os.getenv("AZURE_SQL_PASSWORD", "gkW$;)*w$DJ69J-")

if not all([AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USERNAME, AZURE_SQL_PASSWORD]):
    st.error("Database connection details are not set. Please set the environment variables")
    st.stop()

# connection to database
connection_url = URL.create(
    "mssql+pyodbc",
    username=AZURE_SQL_USERNAME,
    password=AZURE_SQL_PASSWORD,
    host=AZURE_SQL_SERVER,
    port=1433,
    database=AZURE_SQL_DATABASE,
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "Encrypt": "yes",
        "TrustServerCertificate": "no",
        "Connection Timeout": "30",
    },
)

engine = create_engine(connection_url)

# cached data loading

@st.cache_data(ttl=3600)
def load_data():
    query = "SELECT * FROM police_data_cleaned"
    return pd.read_sql(query, engine)

with st.spinner("Loading data from Azure SQL database..."):
    df = load_data()

st.success("Data loaded successfully!")

# sidebar filters
st.sidebar.header("Filters")

crime_types = sorted(df["crime_type"].dropna().unique())
selected_types = st.sidebar.multiselect("Crime type", crime_types, default=crime_types)

months = sorted(df["month"].dropna().unique())
if months:
    selected_months = st.sidebar.select_slider(
        "Month range",
        options=months,
        value=(months[0], months[-1]),
    )
else:
    selected_months = None

# apply filters to the data
filtered = df[df["crime_type"].isin(selected_types)]
if selected_months:
    filtered = filtered[
        (filtered["month"] >= selected_months[0]) & (filtered["month"] <= selected_months[1])
    ]

st.markdown(f"### Showing {len(filtered):,} of {len(df):,} records based on filters ")

########################### Line chart: crime over time ##############
col1, col2 = st.columns(2)

with col1:
    st.subheader("Crimes over time (2024-2026)")
    by_month = filtered.groupby("month").size().sort_index()
    st.line_chart(by_month)



############## Bar chart: crimes by area (LSOA) ##############
st.subheader("Crimes by area (LSOA)")
by_area = (
    filtered.groupby("lsoa_name").size().sort_values(ascending=False).head(15).reset_index(name="count")
)
area_chart = alt.Chart(by_area).mark_bar().encode(
    x=alt.X("count:Q", title="Count", axis=alt.Axis(titleFontSize=17, titleFontWeight="bold")),
    y=alt.Y("lsoa_name:N", sort="-x", title="LSOA", axis=alt.Axis(titleFontSize=17, titleFontWeight="bold")),
    color=alt.Color(
        "count:Q",
        scale=alt.Scale(
            domain=[by_area["count"].min(), by_area["count"].max()],
            range=["#b6bfce", "#1a223c"]
        ),
        legend=None,
    ),
    tooltip=["lsoa_name", "count"],
)
st.altair_chart(area_chart, use_container_width=True)



############### Bar chart: crimes by type ##############
st.subheader("Crimes by type")
by_type = (
    filtered.groupby("crime_type").size().sort_values(ascending=False).head(15).reset_index(name="count")
)
type_chart = (
    alt.Chart(by_type)
    .transform_window(
        rank="rank(count)",
        sort=[alt.SortField("count", order="descending")],
    )
    .mark_bar()
    .encode(
        x=alt.X("count:Q", title="Count", axis=alt.Axis(titleFontSize=17, titleFontWeight="bold")),
        y=alt.Y(
            "crime_type:N",
            sort="-x",
            title="Crime Type",
            axis=alt.Axis(titleFontSize=17, titleFontWeight="bold", labelLimit=0, labelAngle=0),
        ),
        color=alt.Color(
            "count:Q",
            scale=alt.Scale(
                domain=[by_type["count"].min(), by_type["count"].max()],
                range=["#b6bfce", "#1a223c"]
            ),
            legend=None,
        ),
        tooltip=["crime_type", "count"],
    )
)
st.altair_chart(type_chart, use_container_width=True)



############## Map of crime locations ##############
st.subheader("Crime locations")
map_df = filtered.dropna(subset=["latitude", "longitude"])[["latitude", "longitude"]]
if not map_df.empty:
    st.map(map_df)
else:
    st.info("No location data available for the selected filters")