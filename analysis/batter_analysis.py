import pandas as pd
import streamlit as st

from utils.player_data import BASE_DIR, load_player_metadata


BALL_BY_BALL_PATH = (
    BASE_DIR / "data" / "raw" / "ipl_ball_by_ball_2008_2026.csv"
)


@st.cache_data(show_spinner="Loading batter runs by season...")
def aggregate_batter_runs_by_season():
    deliveries = pd.read_csv(
        BALL_BY_BALL_PATH,
        usecols=[
            "season",
            "batter",
            "batter_runs",
            "is_super_over",
            "extra_type",
            "player_out",
        ],
    )
    regular_deliveries = deliveries.loc[
        ~deliveries["is_super_over"].fillna(False)
    ].copy()
    regular_deliveries["balls_faced"] = (
        ~regular_deliveries["extra_type"]
        .fillna("")
        .str.contains("wides", case=False)
    )

    batter_runs = (
        regular_deliveries
        .groupby(["season", "batter"], as_index=False)["batter_runs"]
        .sum()
        .rename(
            columns={
                "batter": "canonical_name",
                "batter_runs": "runs",
            }
        )
    )
    balls_faced = (
        regular_deliveries
        .groupby(["season", "batter"], as_index=False)["balls_faced"]
        .sum()
        .rename(columns={"batter": "canonical_name"})
    )
    dismissals = (
        regular_deliveries
        .dropna(subset=["player_out"])
        .groupby(["season", "player_out"])
        .size()
        .rename("dismissals")
        .reset_index()
        .rename(columns={"player_out": "canonical_name"})
    )

    batter_stats = (
        batter_runs
        .merge(balls_faced, on=["season", "canonical_name"], how="left")
        .merge(dismissals, on=["season", "canonical_name"], how="left")
    )
    batter_stats["dismissals"] = batter_stats["dismissals"].fillna(0)
    batter_stats["strike_rate"] = (
        batter_stats["runs"]
        .div(batter_stats["balls_faced"])
        .mul(100)
        .where(batter_stats["balls_faced"].ne(0))
    )
    batter_stats["batting_average"] = batter_stats["runs"].div(
        batter_stats["dismissals"].replace(0, float("nan"))
    )
    return batter_stats


def _get_canonical_names(player_name, player_metadata_df):
    normalized_name = " ".join(str(player_name).split()).casefold()
    metadata_names = (
        player_metadata_df["full_name"]
        .fillna("")
        .astype(str)
        .map(lambda name: " ".join(name.split()).casefold())
    )
    return (
        player_metadata_df.loc[
            metadata_names == normalized_name, "canonical_name"
        ]
        .dropna()
        .unique()
    )


def get_batter_season_stats(
    player_name,
    batter_stats_by_season,
    player_metadata_df=None,
):
    """Return one batter's seasonal runs, strike rate, and batting average."""
    columns = [
        "season",
        "runs",
        "balls_faced",
        "dismissals",
        "strike_rate",
        "batting_average",
    ]
    empty_result = pd.DataFrame(columns=columns)
    if not player_name or batter_stats_by_season.empty:
        return empty_result

    if player_metadata_df is None:
        player_metadata_df = load_player_metadata()

    canonical_names = _get_canonical_names(player_name, player_metadata_df)
    if len(canonical_names) == 0:
        return empty_result

    player_stats = batter_stats_by_season.loc[
        batter_stats_by_season["canonical_name"].isin(canonical_names)
    ]
    if player_stats.empty:
        return empty_result

    if len(canonical_names) > 1:
        player_stats = (
            player_stats
            .groupby("season", as_index=False)[
                ["runs", "balls_faced", "dismissals"]
            ]
            .sum()
        )
        player_stats["strike_rate"] = (
            player_stats["runs"]
            .div(player_stats["balls_faced"])
            .mul(100)
            .where(player_stats["balls_faced"].ne(0))
        )
        player_stats["batting_average"] = player_stats["runs"].div(
            player_stats["dismissals"].replace(0, float("nan"))
        )

    return (
        player_stats[columns]
        .sort_values("season")
        .reset_index(drop=True)
    )


def get_batter_season_runs(
    player_name,
    batter_runs_by_season,
    player_metadata_df=None,
):
    """Return one player's seasonal runs using the metadata name mapping."""
    empty_result = pd.DataFrame(columns=["season", "runs"])
    if not player_name or batter_runs_by_season.empty:
        return empty_result

    if player_metadata_df is None:
        player_metadata_df = load_player_metadata()

    canonical_names = _get_canonical_names(player_name, player_metadata_df)
    player_runs = batter_runs_by_season.loc[
        batter_runs_by_season["canonical_name"].isin(canonical_names)
    ]
    if player_runs.empty:
        return empty_result

    return (
        player_runs
        .groupby("season", as_index=False)["runs"]
        .sum()
        .sort_values("season")
        .reset_index(drop=True)
    )
