import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(
    page_title="Air Quality Prediction", 
    page_icon=":bar_chart:", 
    layout="centered") #wide

df = pd.read_csv("../air_quality.csv")
df = df.sort_values(by=["date"], ascending=False)
df["date_id"] = df.groupby(["site", "parameter"]).cumcount()+1 

# sidebar
st.sidebar.header("Please Filter Here:")

site = st.sidebar.multiselect(
    "Select positions:",
    options=df["site"].unique(),
    default="Lincoln"
)

param = st.sidebar.multiselect(
    "Select air pollutants: ",
    options=df["parameter"].unique(),
    default="PM25"
)

number = st.sidebar.number_input(
    "Input the number of days:",
    value = 10,
    placeholder="Type a number..."
)
# filter data
df_selection = df.query(
    "site == @site & parameter == @param & date_id <= @number"
)
# st.dataframe(df_selection)

# mainpage
st.title(":bar_chart: Air Quality Watcher —— Predict")
st.markdown("##") # seperate title 
