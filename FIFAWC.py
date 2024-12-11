import pandas as pd
import altair as alt
import streamlit as st
import datetime as dt
import pytz
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Initialize session state for page navigation if not already set
if "current_page" not in st.session_state:
    st.session_state.current_page = "fifaWorldCupHome"  # Start on the home page

# Sidebar navigation
st.sidebar.subheader("Navigation")
fifaWorldCupHome_button = st.sidebar.button(
    "FIFA World Cup Home", 
    on_click=lambda: st.session_state.update({"current_page": "fifaWorldCupHome"})
)
fifaWorldCupData_button = st.sidebar.button(
    "FIFA World Cup Data", 
    on_click=lambda: st.session_state.update({"current_page": "fifaWorldCupData"})
)

# Sidebar for team selection (Shared for both pages)
st.sidebar.header("Filtered Teams")

# Load and display dataset
@st.cache_data
def load_dataset(url):
    df = pd.read_csv(url, encoding='ISO-8859-1')
    return df

dfFIFA = load_dataset("https://raw.githubusercontent.com/GONESIR/Road-To-World-Cup-2026-American-Edition/refs/heads/main/Data/decision.csv")

# Convert 'date' column to datetime format
dfFIFA['date'] = pd.to_datetime(dfFIFA['date'], errors='coerce')

# Extract year from the 'date' column
dfFIFA['year'] = dfFIFA['date'].dt.year

# Filter the teams and show in the sidebar
teams = sorted(set(dfFIFA['home_team']).union(dfFIFA['away_team']))

# Set selected team in session state
if 'selected_team' not in st.session_state:
    st.session_state.selected_team = teams[0]  # Default to first team if no selection

# Sidebar selectbox for team selection
selected_team = st.sidebar.selectbox("Select a team", teams, index=teams.index(st.session_state.selected_team))
st.sidebar.markdown("""*Please note that selected team will only show up in the world cup table only if it has once participated in a tournament.""")

# Update session state when team is selected
st.session_state.selected_team = selected_team


# Home page function
def fifaWorldCupHome():
    st.title("The FIFA World Cup Is Coming to the :red[United] :blue[States]. Are you ready?")
    st.subheader("In preparation for the world's biggest game and tournament, let's take a look at its story")
    st.markdown("""This Streamlit app aims to highlight international football data from 1872 to the last World Cup held in 2022.""")

    # Set timezone to 'America/New_York'
    timezone = pytz.timezone("America/New_York")
    actual_date = datetime.now(timezone)

    # Target date: June 11th, 2026
    target_date = datetime(2026, 6, 11, 0, 0, 0, 0)
    target_date = timezone.localize(target_date)  # Make target_date aware

    # Calculate time remaining
    time_remaining = target_date - actual_date
    days_until = time_remaining.days
    hours_until = time_remaining.seconds // 3600
    minutes_until = (time_remaining.seconds % 3600) // 60
    seconds_until = time_remaining.seconds % 60

    st.markdown(f"""
        <h1>
            <span style='color: red;'>{days_until} days,</span> 
            <span style='color: #0066b2;'>{hours_until} hours,</span>
            <span style='color: red;'>{minutes_until} minutes,</span>
            <span style='color: #0066b2;'> and {seconds_until} seconds</span>
            <span style='color: black;'> until the 2026 FIFA world cup!</span>
        </h1>
    """, unsafe_allow_html=True)

    # Display image and description
    st.image("images/Screenshot 2024-11-25 090400.png")
    st.markdown("""The 2026 FIFA World Cup, which will feature 48 teams, will have 104 games—40 more than the previous 64-game format used in 2022, when there were only 32 teams. This expansion aims to accommodate more teams while retaining the traditional group-stage format with four teams per group​.""")

   

# FIFA World Cup data page function
def fifaWorldCupData():
    
    st.markdown(
        """
        <h1 style='text-align: center;'>
            <span style='color: black;'>The World's Most Prestigious Event: </span>
            <span style='color: gold;'>The World Cup</span>
        </h1>
        """,
        unsafe_allow_html=True
    )

     # Centered Trophy Image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("images/football-background-grass-with-trophy.jpg")

    st.markdown("""The 18-carat gold prize that all nations in the world vie for.""")

    # Load data
    dfResults = load_dataset("https://raw.githubusercontent.com/GONESIR/Road-To-World-Cup-2026-American-Edition/refs/heads/main/Data/decision.csv")

    # Filter for World Cup matches
    if 'tournament' in dfResults.columns:
        world_cup_data = dfResults[dfResults['tournament'] == "FIFA World Cup"]
    else:
        st.warning("The dataset does not contain a 'tournament' column. Please check the data source.")
        world_cup_data = pd.DataFrame()

    # Display Raw Data (Optional)
    if not world_cup_data.empty:
        if st.checkbox("Show World Cup Data"):
            # Filter world cup data for the selected team
            world_cup_team_data = world_cup_data[
                (world_cup_data['home_team'] == st.session_state.selected_team) | 
                (world_cup_data['away_team'] == st.session_state.selected_team)
            ]
            st.dataframe(world_cup_team_data)
    else:
        st.warning("No data available for World Cup matches.")
        
    # Filter data for the selected team (for team-specific analysis)
    team_data = dfFIFA[
        (dfFIFA['home_team'] == st.session_state.selected_team) | 
        (dfFIFA['away_team'] == st.session_state.selected_team)
    ]

    # Calculate wins for the selected team using np.where
    team_data['wins'] = np.where(
        (team_data['home_team'] == st.session_state.selected_team) & 
        (team_data['home_score'] > team_data['away_score']),
        1, 
        np.where(
            (team_data['away_team'] == st.session_state.selected_team) & 
            (team_data['away_score'] > team_data['home_score']),
            1,
            0
        )
    )

    # Summarize wins by year
    wins_by_year = team_data.groupby('year', as_index=False)['wins'].sum()

    # Display filtered team data and wins by year
    st.write("Filtered data for selected team:", team_data)



    # 1. Total Matches by Year
    if not world_cup_data.empty:
        st.markdown("### Total Matches Played by Year")
        world_cup_data['year'] = pd.to_datetime(world_cup_data['date']).dt.year
        matches_by_year = world_cup_data['year'].value_counts().sort_index()

        fig1, ax1 = plt.subplots(figsize=(10, 6))
        matches_by_year.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Number of Matches")
        ax1.set_title("Number of FIFA World Cup Matches by Year")
        st.pyplot(fig1)
    else:
        st.warning("Cannot plot matches by year as no data is available.")

    # 2. Top 10 Teams with Most Wins
    if not world_cup_data.empty:
        st.markdown("### Top 10 Teams with Most Wins")
        top_winners = world_cup_data['home_team'].value_counts().head(10)

        fig2, ax2 = plt.subplots(figsize=(10, 6))
        top_winners.plot(kind='barh', color='gold', ax=ax2)
        ax2.set_xlabel("Number of Wins")
        ax2.set_ylabel("Teams")
        ax2.set_title("Top 10 Winning Teams in FIFA World Cup")
        st.pyplot(fig2)
    else:
        st.warning("Cannot plot top winners as no data is available.")

    # 3. Goals Analysis
    st.markdown("### Goals Scored by Teams")
    if 'home_score' in dfResults.columns and 'away_score' in dfResults.columns and not world_cup_data.empty:
        world_cup_data['total_goals'] = world_cup_data['home_score'] + world_cup_data['away_score']
        total_goals = world_cup_data.groupby('year')['total_goals'].sum()

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        total_goals.plot(kind='line', marker='o', color='green', ax=ax3)
        ax3.set_xlabel("Year")
        ax3.set_ylabel("Total Goals")
        ax3.set_title("Total Goals Scored in the FIFA World Cup by Year")
        st.pyplot(fig3)
    else:
        st.warning("The dataset is missing `home_score` or `away_score` columns for goals analysis.")

    # 4. Match Locations
    if not world_cup_data.empty:
        st.markdown("### Matches by Location")
        if 'city' in dfResults.columns:
            match_locations = world_cup_data['city'].value_counts().head(10)

            fig4 = px.bar(
                x=match_locations.index, 
                y=match_locations.values, 
                title="Top 10 Cities Hosting FIFA World Cup Matches",
                labels={'x': 'City', 'y': 'Number of Matches'},
                color=match_locations.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig4)
        else:
            st.warning("The dataset is missing a `city` column for match locations.")
    else:
        st.warning("Cannot analyze match locations as no data is available.")




# Map pages to functions
fn_map = {
    "fifaWorldCupHome": fifaWorldCupHome,
    "fifaWorldCupData": fifaWorldCupData,
}

# Render the current page
fn_map.get(st.session_state.current_page, fifaWorldCupHome)()
