import plotly.graph_objects as go
import streamlit as st


PLOTLY_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "doubleClick": False,
    "staticPlot": False,
}


def _season_axis(seasons):
    tick_seasons = [seasons[0]]
    for season in seasons[1:]:
        if season - tick_seasons[-1] >= 4:
            tick_seasons.append(season)
    if tick_seasons[-1] != seasons[-1]:
        tick_seasons.append(seasons[-1])

    return {
        # "title": "IPL Season",
        "tickmode": "array",
        "tickvals": tick_seasons,
        "ticktext": [str(season) for season in tick_seasons],
        "range": [min(seasons) - 0.3, max(seasons) + 0.3],
        "showline": True,
        "linecolor": "#A0A0A0",
        "linewidth": 1.5,
        "ticks": "outside",
        "ticklen": 7,
        "showgrid": False,
    }


def _season_metric_figure(season_stats, metric, y_title, hovertemplate):
    seasons = season_stats["season"].tolist()
    figure = go.Figure(
        go.Scatter(
            x=seasons,
            y=season_stats[metric],
            mode="lines+markers",
            line={"color": "#8957FF", "width": 2.5},
            marker={"color": "#8957FF", "size": 7, "symbol": "circle"},
            showlegend=False,
            hovertemplate=hovertemplate,
        )
    )
    figure.update_layout(
        template="plotly_dark",
        height=260,
        margin={"t": 0, "b": 50, "l": 50, "r": 20},
        hovermode="closest",
        dragmode=False,
        hoverlabel={
            "bgcolor": "#252525",
            "bordercolor": "#777777",
            "font": {"color": "white", "size": 13},
            "align": "left",
        },
        showlegend=False,
        xaxis=_season_axis(seasons),
        yaxis={
            "title": y_title,
            "showline": True,
            "linecolor": "#A0A0A0",
            "linewidth": 1.5,
            "ticks": "outside",
            "ticklen": 7,
            "showgrid": True,
            "gridcolor": "#303642",
        },
    )
    return figure


def render_batter_season_chart(player_name, season_runs):
    """Render a batter's runs by IPL season."""
    if season_runs.empty:
        st.info(f"No seasonal run data available for {player_name}.")
    else:
        seasons = season_runs["season"].tolist()
        figure = go.Figure(
            go.Scatter(
                x=seasons,
                y=season_runs["runs"],
                mode="lines+markers",
                line={"color": "#8B5CF6", "width": 2},
                marker={"color": "#8B5CF6", "size": 8, "symbol": "circle"},
                showlegend=False,
                hovertemplate=(
                    "Season: %{x:.0f}<br>"
                    "Runs: %{y:.0f}<extra></extra>"
                ),
            )
        )
        figure.update_layout(
            template="plotly_dark",
            height=360,
            margin={"t": 0},
            hovermode="closest",
            dragmode=False,
            hoverlabel={
                "bgcolor": "#252525",
                "bordercolor": "#777777",
                "font": {"color": "white", "size": 13},
                "align": "left",
            },
            showlegend=False,
            xaxis={
                **_season_axis(seasons),
                "tickmode": "linear",
                "tick0": min(seasons),
                "dtick": 1,
                "tickvals": None,
                "ticktext": None,
            },
            yaxis={
                "title": "Runs",
                "showline": True,
                "linecolor": "#A0A0A0",
                "linewidth": 1.5,
                "ticks": "outside",
                "ticklen": 7,
                "rangemode": "tozero",
            },
        )
        st.plotly_chart(
            figure,
            width="stretch",
            config=PLOTLY_CONFIG,
            key="batter-runs-by-season",
        )


def render_batter_season_metric_charts(player_name, season_stats):
    """Render a batter's seasonal strike rate and batting average."""
    if season_stats.empty:
        st.info(f"No seasonal batting metrics available for {player_name}.")
        return

    strike_rate, batting_average = st.columns(2, gap="large")
    with strike_rate:
        st.subheader("Strike Rate by Season")
        figure = _season_metric_figure(
            season_stats,
            "strike_rate",
            "Strike Rate",
            (
                "Season : %{x:.0f}<br>"
                "SR : %{y:.2f}<br>"
                "<extra></extra>"
            ),
        )
        figure.update_traces(
            customdata=season_stats[["runs", "balls_faced"]]
        )
        figure.update_yaxes(range=[50, 300], dtick=50)
        st.plotly_chart(
            figure,
            width="stretch",
            config=PLOTLY_CONFIG,
            key="batter-strike-rate-by-season",
        )

    with batting_average:
        st.subheader("Average by Season")
        figure = _season_metric_figure(
            season_stats,
            "batting_average",
            "Batting Average",
            (
                "Season: %{x:.0f}<br>"
                "Avg. : %{y:.2f}<br>"
                "<extra></extra>"
            ),
        )
        figure.update_traces(
            customdata=season_stats[["runs", "dismissals"]]
        )
        figure.update_yaxes(rangemode="tozero", tick0=10, dtick=10)
        st.plotly_chart(
            figure,
            width="stretch",
            config=PLOTLY_CONFIG,
            key="batter-average-by-season",
        )
