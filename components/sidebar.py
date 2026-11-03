import streamlit as st
from streamlit_option_menu import option_menu   # pip install streamlit-option-menu

from utils.helpers import load_image


# ---------- sidebar ----------
def render_sidebar():

    background = load_image("assets/images/sidebar_bg.png")
    logo = load_image("assets/images/logo.png")   # optional

    bg_image = f', url("{background}")' if background else ""

    st.markdown(
        f"""
        <style>
        /* ===== Sidebar background (full image, anchored at bottom) ===== */
        section[data-testid="stSidebar"] {{
            background-color: #14143A !important;
            background-image: linear-gradient(
                                  rgba(15,18,48,0.10),
                                  rgba(15,18,48,0.10)
                              ){bg_image} !important;
            background-size: 100% 100%, 100% auto !important;
            background-position: center, bottom center !important;
            background-repeat: no-repeat, no-repeat !important;
        }}

        section[data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebarContent"] {{
            background: transparent !important;
        }}

        /* Header (collapse « button): float it so it no longer pushes content down */
        [data-testid="stSidebarHeader"] {{
            position: absolute !important;
            top: 6px;
            right: 6px;
            height: auto !important;
            padding: 0 !important;
            z-index: 5;
            background: transparent !important;
        }}

        /* Pull everything to the top */
        [data-testid="stSidebarUserContent"] {{
            padding-top: 1.2rem !important;
        }}

        /* nav menu lives in an iframe: keep it see-through */
        section[data-testid="stSidebar"] iframe {{
            color-scheme: normal;
            background: transparent !important;
        }}

        /* ===== Branding (left edge lines up with the nav icons) ===== */
        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 0 14px 16px;
        }}
        .sidebar-brand img {{
            width: 52px;
            height: 52px;
            object-fit: contain;
        }}
        .sidebar-brand .emoji {{
            font-size: 38px;
            line-height: 1;
        }}
        .sidebar-brand .title {{
            color: white;
            font-size: 30px;
            font-weight: 800;
            line-height: 1.05;
        }}
        .sidebar-brand .title span {{
            display: block;
            font-size: 22px;
            font-weight: 400;
            color: #E5E7EB;
        }}

        /* ===== Divider ===== */
        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.15);
            margin: 14px 0;
        }}

        /* ===== Field label ===== */
        .sidebar-label {{
            color: #E5E7EB;
            font-size: 17px;
            font-weight: 500;
            margin: 0 0 8px 2px;
        }}

        /* ===== Select box (light, like the reference) ===== */
        section[data-testid="stSidebar"] div[data-baseweb="select"],
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div > div,
        section[data-testid="stSidebar"] div[data-baseweb="select"] input {{
            background-color: #F5F5FF !important;
            color: #1E1B4B !important;
            -webkit-text-fill-color: #1E1B4B !important;
            font-weight: 500;
        }}
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            border: none !important;
            border-radius: 10px !important;
            min-height: 44px;
        }}
        section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
            fill: #1E1B4B !important;
            color: #1E1B4B !important;
        }}

        /* dropdown list (renders outside the sidebar) */
        div[data-baseweb="popover"] ul[role="listbox"] {{
            background: #F5F5FF !important;
        }}
        div[data-baseweb="popover"] li {{
            background: transparent;
            color: #1E1B4B !important;
        }}
        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li[aria-selected="true"] {{
            background: #E4E1FF !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:

        # Logo / Branding
        logo_html = (
            f'<img src="{logo}">' if logo else '<div class="emoji">🏏</div>'
        )
        st.markdown(
            f"""
            <div class="sidebar-brand">
                {logo_html}
                <div class="title">IPL<span>Analysis</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation (icons are Bootstrap icon names).
        # NOTE: "!important" is required, the library's defaults use it.
        selected_page = option_menu(
            menu_title=None,
            options=[
                "Overall Analysis",
                "Batter Analysis",
                "Bowler Analysis",
                "Season Analysis",
            ],
            icons=["house", "person-fill", "record-circle", "calendar3"],
            default_index=0,
            key="main_nav",
            styles={
                "container": {
                    "padding": "30px 0 0 !important",
                    "background": "transparent !important",
                    "background-color": "transparent !important",
                    "border-radius": "0 !important",
                },
                "icon": {
                    "color": "white !important",
                    "font-size": "18px !important",
                },
                "nav-link": {
                    "font-size": "15px",
                    "font-weight": "500",
                    "color": "#E5E7EB",
                    "text-align": "left",
                    "margin": "6px 0",
                    "padding": "12px 16px",
                    "border-radius": "12px",
                    "background-color": "transparent !important",
                    "--hover-color": "rgba(255,255,255,0.08)",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(90deg, #7145E8, #5932D0)",
                    "color": "white",
                    "font-weight": "600",
                    "box-shadow": "0 3px 12px rgba(105,65,225,0.40)",
                },
            },
        )

        st.html(
                        """
                        <script>
                        (function () {
                        window.__iplMenuBackgroundObserver?.disconnect();
                        const styledMenuFrames = new WeakSet();
                        const applyMenuBackground = () => {
                            const frame = document.querySelector(
                                'iframe[src*="streamlit_option_menu.option_menu"]'
                            );
                            if (!frame || styledMenuFrames.has(frame)) return;
                            const clearBackground = () => {
                                frame.contentDocument?.body?.style.setProperty(
                                    "background-color", "transparent", "important"
                                );
                            };
                            frame.addEventListener("load", clearBackground);
                            clearBackground();
                            styledMenuFrames.add(frame);
                        };
                        window.__iplMenuBackgroundObserver = new MutationObserver(applyMenuBackground);
                        window.__iplMenuBackgroundObserver.observe(document.body, {
                            childList: true,
                            subtree: true
                        });
                        applyMenuBackground();
                        })();
                        </script>
                        """,
                        unsafe_allow_javascript=True,
                )

        st.divider()

        filters = {
            "Batter Analysis": (
                "Batter",
                [
                    "Virat Kohli",
                    "Rohit Sharma",
                    "MS Dhoni",
                    "AB de Villiers",
                    "Suresh Raina",
                ],
            ),
            "Bowler Analysis": (
                "Bowler",
                [
                    "Jasprit Bumrah",
                    "Yuzvendra Chahal",
                    "Bhuvneshwar Kumar",
                    "Lasith Malinga",
                    "Rashid Khan",
                ],
            ),
            "Season Analysis": (
                "Season",
                [str(year) for year in range(2008, 2027)],
            ),
        }

        selected_filter = None
        if selected_page in filters:
            filter_label, options = filters[selected_page]
            st.markdown(
                f'<div class="sidebar-label">{filter_label}</div>',
                unsafe_allow_html=True,
            )
            selected_filter = st.selectbox(
                filter_label,
                options,
                label_visibility="collapsed",
                key=f"{selected_page}_filter",
            )

    return selected_page, selected_filter