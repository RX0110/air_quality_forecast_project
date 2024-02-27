import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import matplotlib.pyplot as plt

#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(
    page_title="Air Quality Prediction", 
    page_icon="📔", 
    layout="centered") #wide

df = pd.read_csv("../air_quality.csv")
df = df.sort_values(by=["date"], ascending=False)
df["date_id"] = df.groupby(["site", "parameter"]).cumcount()+1 

# st.session_state["df"] = df

# sidebar
st.sidebar.header("Please Filter Here:")

site = st.sidebar.selectbox(
    "Select positions:",
    options=df["site"].unique(),
    # default="Lincoln"
    placeholder="Select city...",
)

if site == []:
    parameter_choose = df["parameter"].unique()
else:
    parameter_choose = df[df['site']==site]['parameter'].unique()
    
param = st.sidebar.selectbox(
    "Select air pollutants: ",
    options= parameter_choose,
    #default=parameter_choose[0]
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
st.title(":bar_chart: Air Quality Watcher —— Plots")
st.markdown("##") # seperate title 



tab1, tab2, tab3 = st.tabs(["📈 Previous Pollution Index Line Plot", "📊 Number of days for each description", "Data"])

with tab1:
   # line chart
    try: 
        # if(len(param) > 1):
        #     for p in param:
        #         temp_df = df_selection[df_selection["parameter"]== p]
        #         plt.plot(temp_df["date"], temp_df["index_value"])
        #         plt.title(f"Line plot of {param[0]} for site {site[0]}")
        #     st.pyplot(plt)
        # else:
        #     st.header(f"Line plot of {param[0]} for site {site[0]}")
        #     st.line_chart(data=df_selection, x="date", y="index_value", color=None, width=0, height=0, use_container_width=True)
        st.header(f"Line plot of {param[0]} for site {site[0]}")
        st.line_chart(data=df_selection, x="date", y="index_value", color=None, width=0, height=0, use_container_width=True)
    except IndexError:
        st.error("Please choose a valid input")
 
with tab2:
   # bar chart
   number_by_description = df_selection.groupby(by=["description"]).size()
   # Convert the Series to a DataFrame and reset the index
   number_by_description_df = number_by_description.reset_index(name='count')
   fig = px.bar(number_by_description_df, x='description', y='count',
                title="<b>Number of days for each description level</b>",
                color="description",
                text_auto = True)
   fig.update_traces(textfont_size = 20, textangle = 0)
   st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with tab3:
   st.dataframe(df_selection)
