from pathlib import Path
import re

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PLAYER_IMAGE = "assets/images/players/player.png"


@st.cache_data
def load_player_metadata():
    csv_path = BASE_DIR / "data" / "processed" / "player_metadata.csv"
    return pd.read_csv(csv_path)


TEAM_BANNERS = {
    "Royal Challengers Bengaluru": "assets/images/team_banners/rcb_banner.png",
    "Chennai Super Kings": "assets/images/team_banners/csk_banner.png",
    "Rajasthan Royals": "assets/images/team_banners/rr_banner.png",
    "Gujarat Titans": "assets/images/team_banners/gt_banner.png",
    "Mumbai Indians": "assets/images/team_banners/mi_banner.png",
    "Delhi Capitals": "assets/images/team_banners/dc_banner.png",
    "Kolkata Knight Riders": "assets/images/team_banners/kkr_banner.png",
    "Lucknow Super Giants": "assets/images/team_banners/lsg_banner.png",
    "Punjab Kings": "assets/images/team_banners/pbks_banner.png",
    "Sunrisers Hyderabad": "assets/images/team_banners/srh_banner.png",
}

DEFAULT_TEAM_BANNER = TEAM_BANNERS["Royal Challengers Bengaluru"]


def _normalized_name(value):
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def get_player_image_path(player_name):
    """Resolve an existing player image or return the default silhouette."""
    normalized_name = _normalized_name(player_name)
    if not normalized_name:
        return DEFAULT_PLAYER_IMAGE

    relative_path = (
        Path("assets")
        / "images"
        / "players"
        / f"{normalized_name}.png"
    )
    if (BASE_DIR / relative_path).is_file():
        return str(relative_path)

    return DEFAULT_PLAYER_IMAGE


def get_team_banner_path(team_name):
    """Resolve a team's banner, falling back to the default banner if needed."""
    normalized_team = " ".join(str(team_name).split()).casefold()
    for mapped_team, banner_path in TEAM_BANNERS.items():
        if " ".join(mapped_team.split()).casefold() == normalized_team:
            if (BASE_DIR / banner_path).is_file():
                return banner_path
            break

    return DEFAULT_TEAM_BANNER


def get_batter_options(player_metadata_df):
    return (
        player_metadata_df
        .dropna(subset=["full_name"])
        .sort_values("batter_runs", ascending=False)
        .drop_duplicates(subset="canonical_name")
        .query("full_name != 'No information available'")
        ["full_name"]
        .tolist()
    )


def get_bowler_options(player_metadata_df):
    return (
        player_metadata_df
        .dropna(subset=["full_name"])
        .sort_values("is_wicket", ascending=False)
        .drop_duplicates(subset="canonical_name")
        .query("full_name != 'No information available'")
        ["full_name"]
        .tolist()
    )
