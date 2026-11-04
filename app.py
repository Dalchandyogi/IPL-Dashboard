
import streamlit as st

from components.sidebar import render_sidebar
from components.player_info_card import render_player_card
from utils.player_data import PLAYER_IMAGES, PLAYER_TEAMS, TEAM_BANNERS


# Page Configuration
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.html(
    """
    <style>
    section[data-testid="stMain"] [data-testid="stMainBlockContainer"] {
        padding-top: 16px !important;
    }
    </style>
    """
)


# Render Sidebar
page, selected_filter = render_sidebar()


# Main Content
st.title(page)


# Filter Labels
filter_labels = {
    "Batter Analysis": "Batter",
    "Bowler Analysis": "Bowler",
    "Season Analysis": "Season",
}


# Display Selected Filter
if selected_filter is not None and page in filter_labels:
    st.write(f"Selected {filter_labels[page]}: {selected_filter}")


# Batter Analysis
if page == "Batter Analysis":

    render_player_card(
        player_name="Virat Kohli",
        team_name="Royal Challengers Bengaluru",
        batting_style="Right-hand Batter",
        player_image=PLAYER_IMAGES[selected_filter],
        team_banner=TEAM_BANNERS[PLAYER_TEAMS[selected_filter]],
        debut=2008,
        centuries=9,
        half_centuries=45,
        stats=[
            ("8,000", "Runs"),
            ("134.89", "Strike Rate"),
            ("45.78", "Batting Average"),
            ("250", "Matches"),
            ("113*", "Highest Score"),
        ]
    )
