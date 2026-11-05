
import streamlit as st
from html import escape
import math

from utils.helpers import load_image
from utils.player_data import DEFAULT_PLAYER_IMAGE, DEFAULT_TEAM_BANNER
from components.metric_card import (
    get_metric_card_html,
    get_split_metric_card_html
)


def _is_missing(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"", "nan", "none", "<na>"}
    try:
        return math.isnan(float(value))
    except (TypeError, ValueError, OverflowError):
        return str(value).strip().lower() in {"", "nan", "none", "<na>"}


def _format_profile_value(value, label):
    if _is_missing(value):
        return "—"

    if label in {
        "Runs",
        "Matches",
        "100s",
        "50s",
        "Debut",
        "Highest Score",
    }:
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            return str(value)
        if not math.isfinite(number):
            return "N/A"
        if label == "Runs":
            return f"{int(number):,}"
        return str(int(number))

    if label in {"Strike Rate", "Batting Average"}:
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            return str(value)
        if not math.isfinite(number):
            return "N/A"
        return f"{number:.2f}"

    return str(value)


def render_player_card(
    player_name,
    team_name,
    batting_style,
    player_image,
    team_banner,
    debut,
    stats,
    centuries,
    half_centuries,
):
    """Render dynamic IPL player profile banner."""

    # Load images
    bg_image = load_image(team_banner) or load_image(DEFAULT_TEAM_BANNER)
    profile_image = load_image(player_image) or load_image(DEFAULT_PLAYER_IMAGE)
    background_style = (
        f'background-image: url("{bg_image}");' if bg_image else ""
    )

    # Player photo
    photo_html = ""

    if profile_image:
        photo_html = f"""
        <img
            src="{profile_image}"
            class="player-photo"
        >
        """

    # Reuse metric card component
    metrics_html = "".join(
        get_metric_card_html(_format_profile_value(value, label), label)
        for value, label in stats
    )
    metrics_html += get_split_metric_card_html(
        _format_profile_value(centuries, "100s"),
        "100s",
        _format_profile_value(half_centuries, "50s"),
        "50s",
    )

    # Player banner HTML
    html = f"""
    <style>


        
        .player-banner {{
            position: relative;
            height: 300px;
            top: -12px;
            width: 100%;
            overflow: hidden;
            border-radius: 15px;
            color: white;

            {background_style}

            background-size: 100% 100%;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .player-photo {{
            position: absolute;
            bottom: -16px;
            left: 8%;
            height: 105%;
            # width: 24%;
            object-fit: contain;
            object-position: bottom;
            z-index: 2;
        }}

        .player-details {{
            position: absolute;
            top: 12%;
            left: 34%;
            z-index: 3;
        }}

        .player-name {{
            font-size: 38px;
            font-weight: 750;
        }}

        .team-name {{
            font-size: 15px;
            margin: 5px 0;
        }}

        .batting-style {{
            display: inline-block;
            background: #285C3D;
            border: 1px solid #8BE0A6;
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 12px;
        }}

        .player-debut {{
            font-size: 12px;
            margin-top: 7px;
            color: #D5D5E5;
        }}

        .player-metrics {{
            position: absolute;
            left: 34%;
            right: 3%;
            bottom: 18px;

            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 12px;
            z-index: 3;
        }}

        .player-metric {{
            background: rgba(34, 57, 91, 0.95);
            border: 1.5px solid rgba(255,255,255,0.9);
            border-radius: 12px;
            min-height: 75px;

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            text-align: center;
            padding: 5px;
            box-sizing: border-box;
        }}

        .metric-value {{
            font-size: 25px;
            font-weight: 600;
        }}

        .metric-label {{
            font-size: 13px;
            color: #E5E7EB;
        }}

        .split-metric {{
            flex-direction: row;
            gap: 0;
        }}

        .split-item {{
            display: flex;
            flex: 1;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-width: 0;
        }}

        .split-divider {{
            width: 1px;
            height: 42px;
            background: rgba(255,255,255,0.65);
        }}
    </style>

    <div class="player-banner">

        {photo_html}

        <div class="player-details">
            <div class="player-name">
                {escape(_format_profile_value(player_name, "Player"))}
            </div>

            <div class="team-name">
                {escape(_format_profile_value(team_name, "Team"))}
            </div>

            <div class="batting-style">
                {escape(_format_profile_value(batting_style, "Batting style"))}
            </div>

            <div class="player-debut">
                IPL Debut: {escape(_format_profile_value(debut, "Debut"))}
            </div>
        </div>

        <div class="player-metrics">
            {metrics_html}
        </div>

    </div>
    """

    # Render HTML directly (not Markdown)
    st.html(html)
