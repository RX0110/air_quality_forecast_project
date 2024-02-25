import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Air Quality Prediction",
    page_icon="☁",
)

st.title("Welcome to Air Quality Watcher 👋")

# if "my_input" not in st.session_state:
#     st.session_state["my_input"] = ""

# my_input = st.text_input("Input a text here", st.session_state["my_input"])
# submit = st.button("Submit")
# if submit:
#     st.session_state["my_input"] = my_input
#     st.write("You have entered: ", my_input)

# side bar 
with st.sidebar:
    selected = option_menu(
        menu_title="Outline Menu",  # required
        options=["Vision", "Health Effect", "Why US"],  # required
        icons=["eye", "book", "question"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
    )


if selected == "Vision":
    st.subheader("Vision")
    st.write("Our vision is to create an air quality forecasting tool, aiding environmental planning, public health advisories, and personal outdoor activity decisions.")
    st.image('img/PM25.jpg', width=400)
if selected == "Health Effect":
    st.subheader("Health Effect")
    st.write("The health effects of air pollution are significant and multifaceted, impacting individuals in both the \
              short and long term. Exposure to pollutants such as particulate matter, nitrogen dioxide, sulfur dioxide, \
              and ozone can lead to respiratory issues, including asthma, bronchitis, and chronic obstructive pulmonary disease (COPD). Long-term exposure is linked to increased rates of cardiovascular diseases, strokes, and lung cancer. Children, the elderly, and individuals with preexisting health conditions are particularly vulnerable. Moreover, air pollution can exacerbate existing health issues, leading to increased hospital admissions and healthcare costs. There is also emerging evidence suggesting that air pollution may impact mental health and cognitive functions, indicating that its effects are even more widespread than previously understood. Reducing air pollution levels is crucial for public health improvement.")
    st.image('img/Effect.jpg')
if selected == "Why US":
    st.subheader("Why US")
    st.write("Our platform is designed to be user-friendly, ensuring you have the information you need, whenever and wherever you need it. \
             Now, you might wonder, 'What makes this product the superior choice over other alternatives in the market?' The answer lies in our \
            localized approach and high-precision algorithms that are tailored to provide the most accurate predictions, which are crucial for individual and community health and wellbeing. We've identified several supporting products and services that can amplify the value our air quality predictions provide. For instance, smart home devices such as air purifiers, HVAC systems, and window controllers can use our data to automatically adjust settings, creating an optimal indoor environment based on real-time air quality levels.")
    st.image('img/smart-home.png')