
import streamlit as st
from html import escape

from utils.helpers import load_image
from components.metric_card import (
    get_metric_card_html,
    get_split_metric_card_html
)


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
    bg_image = load_image(team_banner)
    profile_image = load_image(player_image)

    if not bg_image:
        st.error(f"Banner not found: {team_banner}")
        return

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
        get_metric_card_html(value, label)
        for value, label in stats
    )
    metrics_html += get_split_metric_card_html(
        centuries,
        "100s",
        half_centuries,
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

            background-image:
                url("{bg_image}");

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
                {escape(player_name)}
            </div>

            <div class="team-name">
                {escape(team_name)}
            </div>

            <div class="batting-style">
                {escape(batting_style)}
            </div>

            <div class="player-debut">
                IPL Debut: {escape(str(debut))}
            </div>
        </div>

        <div class="player-metrics">
            {metrics_html}
        </div>

    </div>
    """

    # Render HTML directly (not Markdown)
    st.html(html)
