import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("The Outcomes Of Every International Football Game")

st.subheader(
    "With a rich history spanning over 150 years, every FIFA match tells a unique story of competition, passion, and sporting excellence. "
    "My data compiles the results, team performances, venues, and tournaments, providing a comprehensive view of how the world’s most beloved sport has evolved over time."
)

# Create columns to control the container size
col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is wider

st.image("images/Screenshot 2024-12-09 215205.png", width=1000)  # Adjust the width value as needed

st.markdown("""
    History plays a crucial part in telling this story.
""", unsafe_allow_html=True)

def load_dataset(url):
    df = pd.read_csv(url, encoding='ISO-8859-1')
    return df

dfFIFA = load_dataset("https://raw.githubusercontent.com/GONESIR/Road-To-World-Cup-2026-American-Edition/main/Data/FIFA%20Results.csv")

# Compute total goals for teams - Top 20
st.markdown("### Top 20 Teams with Most Goals Scored")

# Group by team and count the number of goals scored
team_goals = dfFIFA.groupby('team')['scorer'].count().sort_values(ascending=False).head(20)

# Plot the data
fig1, ax1 = plt.subplots(figsize=(10, 6))
team_goals.plot(kind='bar', color='blue', ax=ax1)
ax1.set_xlabel("Team")
ax1.set_ylabel("Goals Scored")
ax1.set_title("Top 20 Teams with Most Goals Scored")
st.pyplot(fig1)


# Goals Scored by Minute
st.markdown("### Goals Scored by Minute")

minute_counts = dfFIFA['minute'].value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
minute_counts.plot(kind='line', marker='o', color='green', ax=ax2)
ax2.set_xlabel("Minute")
ax2.set_ylabel("Number of Goals")
ax2.set_title("Goals Scored by Minute")
st.pyplot(fig2)

# Top Scorers
st.markdown("### Top Scorers")

top_scorers = dfFIFA['scorer'].value_counts().head(10)

fig3, ax3 = plt.subplots(figsize=(10, 6))
top_scorers.plot(kind='barh', color='gold', ax=ax3)
ax3.set_xlabel("Number of Goals")
ax3.set_ylabel("Scorer")
ax3.set_title("Top 10 Scorers")
st.pyplot(fig3)

# Own Goals Analysis - Top 20 Teams
st.markdown("### Top 20 Teams with Own Goals Scored")

# Filter the data to get teams that have scored own goals
own_goal_counts = dfFIFA[dfFIFA['own_goal'] == True]['team'].value_counts().head(20)

# Plot the data
fig5, ax5 = plt.subplots(figsize=(10, 6))
own_goal_counts.plot(kind='bar', color='purple', ax=ax5)
ax5.set_xlabel("Team")
ax5.set_ylabel("Own Goals")
ax5.set_title("Top 20 Teams with Own Goals Scored")
st.pyplot(fig5)

# Goals Over Time
st.markdown("### Goals Scored Over Time")

dfFIFA['year'] = pd.to_datetime(dfFIFA['date']).dt.year
goals_by_year = dfFIFA.groupby('year')['scorer'].count()

fig6, ax6 = plt.subplots(figsize=(10, 6))
goals_by_year.plot(kind='line', marker='o', color='orange', ax=ax6)
ax6.set_xlabel("Year")
ax6.set_ylabel("Total Goals")
ax6.set_title("Goals Scored Over Time")
st.pyplot(fig6)


# Interactive Match Explorer
st.markdown("### Explore Matches")

# Unique teams for filtering
teams = sorted(dfFIFA['team'].unique())

selected_team = st.selectbox("Select a Team to Explore", teams)

team_matches = dfFIFA[dfFIFA['team'] == selected_team]

st.write(f"Matches involving {selected_team}:")
st.dataframe(team_matches)

