import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from random import seed
import pmdarima as pm #auto arima
from statsmodels.tsa.statespace.sarimax import SARIMAX

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

# filter data
df_selection = df.query(
    "site == @site & parameter == @param"
)
# st.dataframe(df_selection)

# mainpage
st.title(":bar_chart: Air Quality Watcher —— Predict")
st.markdown("##") # seperate title 

# st.write(df_selection)

data = df_selection[['date','site', 'parameter','index_value']]
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)
data = data.sort_index()
data = data[data["parameter"].str.contains(param)]
filtered_data = data[(data['site'].str.contains(site))]
polution_site_daily = filtered_data['index_value'].resample('D').mean()
polution_site_daily.dropna(inplace=True)
df_new = polution_site_daily.to_frame(name='value')
# df_new = df_new.reindex(pd.date_range('2016-05-28', '2024-02-17'))
pd.date_range(start = df_new.index.min(), end = df_new.index.max(), freq='MS').difference(df_new.index)
df_new = df_new.interpolate(method='time')

# df_new
# st.write(len(df_new))

test_size = 7
if len(df_new)<= 90 :
    df1 = df_new
else:
    df1 = df_new.iloc[-90:]


smodel1 = SARIMAX(df1['value'], order=(1,0,0), seasonal_order=(2,1,0,7))
fit_results =  smodel1.fit()

previous_data = []

last = df_new.index.max()
day = last.day
month = last.month
predict_period = [f"{month}-{i}" for i in range(day+1, day+9)]
for day in predict_period:
    l = pd.to_datetime([f"{year}-{day}" for year in range(2016, 2024)])
  
    # Step 3: Find missing dates
    missing_dates = l[~l.isin(df.index)]

    # Step 4: Add missing dates with 0 values
    # Create a temporary DataFrame with missing dates and 0 values
    temp_df = pd.DataFrame(index=missing_dates, columns=df_new.columns).fillna(0)

    # Append the temporary DataFrame to the original DataFrame
    df_new = df_new.append(temp_df).sort_index()


    previous_data.append(df_new.loc[l].mean())

#st.write(previous_data)

#predict data
predict_smodel = fit_results.forecast(steps=7)

#st.write(predict_smodel)

predict_data = []
for i in range(len(predict_smodel)):
  #print(predict_smodel[i] + previous_data[i])
  predict_data.append((2/3)*predict_smodel.iloc[i] + (1/3)*float(previous_data[i]))

#st.write(predict_data)

tab1, tab2, tab3 = st.tabs(["📈 Next 7 days prediction line plot", "📊Next 7 days prediction comment", "Data"])
with tab1:
    # try: 
    #     df_plot = pd.DataFrame({"value": predict_data, "day": list(range(1,8))})
    #     st.header(f"Line plot of {param[0]} for site {site[0]}")
    #     st.line_chart(data=df_plot,x="day", y="value", color=None, width=0, height=0, use_container_width=True)
    # except IndexError:
    #     st.error("Please choose a valid input")
    try:
        df_plot = pd.DataFrame({"value": predict_data, "day": list(range(1,8))})
        fig = px.bar(df_plot, x="day", y="value",
                title="<b>Number of days for each description level</b>",
                color_discrete_sequence =['#66B2FF']*3,
                text_auto = True)
        fig.update_traces(textfont_size = 20, textangle = 0)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    except IndexError:
        st.error("Please choose a valid input")

with tab2:
    df_plot = pd.DataFrame({"day": list(range(1,8)), "value": predict_data}).reset_index(drop=True)
    df_plot["level"] = df_plot['value'].apply(lambda x: "😊 good " if x < 35 else "😔 bad")
    st.table(df_plot)

with tab3:
    df_plot = pd.DataFrame({"value": predict_data, "day": list(range(1,8))})
    st.write(df_plot)