import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit page setup
st.set_page_config(layout="wide")
st.title("The Games That Went To :green[Penalty] Shoot Outs")

st.subheader(":green[Penalty] Shoot-outs are when competitive games do not have a winner after regular or extra time. A penalty shoot-out "\
             "contest is conducted. The team with the most successful penalties wins.")




# Display image
st.image("images/Screenshot 2024-12-09 190931.png")

st.markdown("""
    Last world cup's nail-biting final finished in dramatic penalty shoot-outs.
""", unsafe_allow_html=True)
# Load data
def load_dataset(url):
    df = pd.read_csv(url, encoding='ISO-8859-1')
    return df

dfPenaltyShootOuts = load_dataset("https://raw.githubusercontent.com/GONESIR/Road-To-World-Cup-2026-American-Edition/refs/heads/main/Data/penality%20kick.csv")


# Filter by teams involved in penalty shoot-outs (assuming you can flag such games in the data)
# For now, we assume all matches in the dataset were resolved via penalties
penalty_data = dfPenaltyShootOuts.copy()

# 1. Count wins by team
team_wins = penalty_data['winner'].value_counts().head(10)  # Top 10 winning teams

# Visualization: Top 10 Teams in Penalty Shoot-outs
st.markdown("### Top 10 Teams in Penalty Shoot-outs")
fig, ax = plt.subplots(figsize=(10, 6))
team_wins.plot(kind='barh', color='gold', ax=ax)
ax.set_xlabel("Number of Wins")
ax.set_ylabel("Teams")
ax.set_title("Top 10 Winning Teams in Penalty Shoot-outs")
st.pyplot(fig)

# 2. Analysis by Continent
continent_wins = penalty_data.groupby('home_continent')['winner'].count()

# Visualization: Wins by Continent
st.markdown("### Wins by Continent")
fig, ax = plt.subplots(figsize=(8, 5))
continent_wins.plot(kind='bar', color='skyblue', ax=ax)
ax.set_xlabel("Continents")
ax.set_ylabel("Number of Wins")
ax.set_title("Penalty Shoot-out Wins by Continent")
st.pyplot(fig)

# Add filters for interactivity
st.markdown("### Filter Data")
selected_team = st.selectbox("Select a Team", dfPenaltyShootOuts['home_team'].unique())
filtered_data = penalty_data[(penalty_data['home_team'] == selected_team) | (penalty_data['opponent_team'] == selected_team)]
st.write(f"Games involving {selected_team}:")
st.dataframe(filtered_data)
