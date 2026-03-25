import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.title("Analytics Dashboard")

@st.cache_data
def load_data():
    np.random.seed(42)
    data = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=200),
        "Category": np.random.choice(["A", "B", "C"], 200),
        "Value": np.random.randint(10, 500, 200)
    })
    return data

df = load_data()

st.sidebar.header("Filters")

category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())

date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))
col2.metric("Total Value", int(filtered_df["Value"].sum()))
col3.metric("Average Value", round(filtered_df["Value"].mean(), 2))

st.subheader("Time Series Analysis")

line_fig = px.line(filtered_df, x="Date", y="Value", color="Category", title="Value Over Time")
st.plotly_chart(line_fig, use_container_width=True)

st.subheader("Category Distribution")

bar_fig = px.bar(filtered_df.groupby("Category")["Value"].sum().reset_index(), x="Category", y="Value", color="Category")
st.plotly_chart(bar_fig, use_container_width=True)

st.subheader("Raw Data")

st.dataframe(filtered_df, use_container_width=True)
