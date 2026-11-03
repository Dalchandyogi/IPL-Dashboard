
import streamlit as st
from html import escape


def get_metric_card_html(value, label):
    """Return metric card HTML for embedding."""

    return f"""
        <div class="player-metric">
            <div class="metric-value">
                {escape(str(value))}
            </div>
            <div class="metric-label">
                {escape(str(label))}
            </div>
        </div>
    """


def render_metric_card(value, label):
    """Render a standalone metric card."""

    st.markdown(
        f"""
        <style>
        .common-metric-card {{
            background: #22395B;
            border: 1px solid #8998B8;
            border-radius: 12px;
            padding: 18px 10px;
            text-align: center;
            color: white;
        }}

        .common-metric-value {{
            font-size: 25px;
            font-weight: 700;
        }}

        .common-metric-label {{
            font-size: 13px;
            color: #D5DCEC;
        }}
        </style>

        <div class="common-metric-card">
            <div class="common-metric-value">
                {escape(str(value))}
            </div>
            <div class="common-metric-label">
                {escape(str(label))}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



def get_split_metric_card_html(
    left_value,
    left_label,
    right_value,
    right_label
):
    """Return a horizontal split metric card."""

    from html import escape

    return f"""
    <div class="player-metric split-metric">

        <div class="split-item">
            <div class="metric-value">
                {escape(str(left_value))}
            </div>
            <div class="metric-label">
                {escape(str(left_label))}
            </div>
        </div>

        <div class="split-divider"></div>

        <div class="split-item">
            <div class="metric-value">
                {escape(str(right_value))}
            </div>
            <div class="metric-label">
                {escape(str(right_label))}
            </div>
        </div>

    </div>
    """
