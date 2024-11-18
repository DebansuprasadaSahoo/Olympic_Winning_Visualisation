import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
df = pd.read_csv("athlete_events.csv")

# Clean the data: Strip any extra spaces from column names
df.columns = df.columns.str.strip()

# Drop rows where 'Team', 'Sport', or 'Medal' are missing
df.dropna(subset=['Team', 'Sport', 'Medal'], inplace=True)

# Group by Year, Team (Country), Sport, and Medal to count medals
medal_counts = df.groupby(['Year', 'Team', 'Sport', 'Medal']).size().reset_index(name='Count')

# Streamlit App Title
st.title("Olympic Medal Statistics Dashboard")

# Dropdown to select a specific country
country = st.selectbox("Select a Country", df['Team'].unique())

# Filter data based on selected country
country_data = medal_counts[medal_counts['Team'] == country]

# Visualization 1: Medals won by the selected country over the years
st.subheader(f"Medals won by {country} Over the Years")
year_chart = px.bar(country_data, x='Year', y='Count', color='Medal', title=f"Medals won by {country} Over the Years")
st.plotly_chart(year_chart)

# Visualization 2: Medals won by the selected country in different sports
st.subheader(f"Medals won by {country} in Different Sports")
sport_chart = px.bar(country_data, x='Sport', y='Count', color='Medal', title=f"Medals won by {country} in Different Sports")
st.plotly_chart(sport_chart)

# Global Medals: Show a world map of the total medals won by each country
st.subheader("World Medal Distribution")

# Aggregate global data
global_data = medal_counts.groupby(['Team', 'Medal']).agg({'Count': 'sum'}).reset_index()

# Data Table Display - Option to show the full dataset
if st.checkbox("Show Data Table"):
    st.write(medal_counts)

# User Input Section for Year, Country, and Medal
st.subheader("Search Specific Medal Information")
year_input = st.number_input("Enter the Year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), step=1)
country_input = st.text_input("Enter the Country Name")
medal_input = st.selectbox("Select the Medal Type", ["Gold", "Silver", "Bronze"])

if st.button("Find Medal Information"):
    # Filter the dataset based on the inputs
    filtered_data = medal_counts[
        (medal_counts['Year'] == year_input) &
        (medal_counts['Team'].str.contains(country_input, case=False, na=False)) &
        (medal_counts['Medal'] == medal_input)
    ]
    
    if not filtered_data.empty:
        total_medals = filtered_data['Count'].sum()
        st.success(f"In {year_input}, {country_input} won {total_medals} {medal_input.lower()} medal(s).")
    else:
        st.warning(f"No records found for {country_input} winning {medal_input.lower()} medal(s) in {year_input}.")

# Add custom CSS for background image
bg_image_url = "https://e0.365dm.com/24/07/2048x1152/skysports-paris-olympics-eiffel-tower_6636084.jpg?20240722092351"  # Replace with your image URL
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_image_url}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        height: 100vh;
    }}
    </style>
    """, unsafe_allow_html=True)
