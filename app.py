
import streamlit as st

from components.sidebar import render_sidebar
from components.player_info_card import render_player_card
from analysis.batter_analysis import (
    aggregate_batter_runs_by_season,
    get_batter_season_stats,
    get_batter_season_runs,
)
from components.batter_season_chart import (
    render_batter_season_chart,
    render_batter_season_metric_charts,
)
from utils.player_data import (
    get_player_image_path,
    get_team_banner_path,
    load_player_metadata,
)


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


# Load player metadata once, then share it with the sidebar and profile section.
player_metadata_df = load_player_metadata()


# Render Sidebar
page, selected_filter = render_sidebar(player_metadata_df)


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
    # st.write(f"Selected {filter_labels[page]}: {selected_filter}")
    pass


# Batter Analysis
if page == "Batter Analysis":
    st.badge("Showing each batter's latest IPL team")
    player_rows = player_metadata_df.loc[
        player_metadata_df["full_name"] == selected_filter
    ]

    if player_rows.empty:
        st.error(f"No player profile data found for {selected_filter}.")
    else:
        player_row = player_rows.iloc[0]
        player_team = player_row["team"]
        team_banner = get_team_banner_path(player_team)

        render_player_card(
            player_name=player_row["full_name"],
            team_name=player_team,
            batting_style=player_row["batting_style"],
            player_image=get_player_image_path(player_row["full_name"]),
            team_banner=team_banner,
            debut=player_row["debut"],
            centuries=player_row["hundreds"],
            half_centuries=player_row["fifties"],
            stats=[
                (player_row["runs"], "Runs"),
                (player_row["strike_rate"], "Strike Rate"),
                (player_row["batting_average"], "Batting Average"),
                (player_row["matches"], "Matches"),
                (player_row["highest_score_display"], "Highest Score"),
            ],
        )

        st.subheader(f"Runs by IPL Season")
        batter_runs_by_season = aggregate_batter_runs_by_season()
        season_runs = get_batter_season_runs(
            selected_filter,
            batter_runs_by_season,
            player_metadata_df,
        )
        season_stats = get_batter_season_stats(
            selected_filter,
            batter_runs_by_season,
            player_metadata_df,
        )
        render_batter_season_chart(selected_filter, season_runs)
        render_batter_season_metric_charts(selected_filter, season_stats)
