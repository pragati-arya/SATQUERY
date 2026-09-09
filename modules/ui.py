from pathlib import Path
import base64
import streamlit as st


def apply_space_background():

    project_root = Path(__file__).resolve().parent.parent
    image_path = project_root / "assets" / "satquery_space1.png"

    if not image_path.exists():
        st.error(
            f"Background image not found at: {image_path}"
        )
        return

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        /* =====================================================
           GLOBAL APP
        ===================================================== */

        .stApp {{
            background:
                linear-gradient(
                    rgba(3, 8, 20, 0.68),
                    rgba(3, 8, 20, 0.82)
                ),
                url("data:image/png;base64,{encoded_image}") !important;

            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}

        /* Remove Streamlit default top padding */

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 4rem;
            max-width: 1400px;
        }}


        /* =====================================================
           HEADER
        ===================================================== */

        .satquery-header {{
            text-align: center;
            padding: 28px 20px 25px 20px;
            margin-bottom: 25px;

            background: rgba(5, 15, 35, 0.55);
            border: 1px solid rgba(80, 190, 255, 0.25);
            border-radius: 24px;

            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);

            box-shadow:
                0 0 35px rgba(0, 150, 255, 0.12),
                inset 0 0 30px rgba(0, 150, 255, 0.04);
        }}

        .satquery-logo {{
            font-size: 52px;
            font-weight: 900;
            letter-spacing: 3px;

            background: linear-gradient(
                90deg,
                #ffffff,
                #7dd3fc,
                #38bdf8
            );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            text-shadow: 0 0 25px rgba(56, 189, 248, 0.35);
        }}

        .satquery-subtitle {{
            margin-top: 8px;
            font-size: 16px;
            color: rgba(220, 240, 255, 0.82);
            letter-spacing: 0.4px;
        }}

        .status-pill {{
            display: inline-block;
            margin-top: 15px;
            padding: 7px 16px;

            border-radius: 50px;

            background: rgba(0, 190, 255, 0.10);
            border: 1px solid rgba(0, 210, 255, 0.35);

            color: #7dd3fc;
            font-size: 13px;
            font-weight: 600;

            box-shadow: 0 0 18px rgba(0, 190, 255, 0.12);
        }}


        /* =====================================================
           SECTION HEADINGS
        ===================================================== */

        h2, h3 {{
            color: #e8f7ff !important;
        }}

        .section-title {{
            font-size: 22px;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 15px;
        }}


        /* =====================================================
           GLASS CARDS
        ===================================================== */

        .glass-card {{
            background: rgba(7, 18, 38, 0.62);

            border: 1px solid rgba(120, 210, 255, 0.18);
            border-radius: 18px;

            padding: 20px;

            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);

            box-shadow:
                0 12px 35px rgba(0, 0, 0, 0.25),
                inset 0 0 25px rgba(80, 180, 255, 0.025);

            transition: all 0.25s ease;
        }}

        .glass-card:hover {{
            border-color: rgba(100, 210, 255, 0.38);

            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.30),
                0 0 25px rgba(0, 170, 255, 0.08);
        }}


        /* =====================================================
           FILE UPLOADERS
        ===================================================== */

        section[data-testid="stFileUploaderDropzone"] {{
            background: rgba(5, 15, 35, 0.70) !important;

            border: 1px dashed rgba(90, 200, 255, 0.42) !important;
            border-radius: 16px !important;

            min-height: 150px;

            backdrop-filter: blur(12px);
        }}

        section[data-testid="stFileUploaderDropzone"]:hover {{
            border-color: rgba(100, 220, 255, 0.75) !important;

            box-shadow:
                0 0 25px rgba(0, 170, 255, 0.10);
        }}


        /* =====================================================
           QUERY BOX
        ===================================================== */

        div[data-baseweb="input"] {{
            background: rgba(5, 15, 35, 0.70) !important;

            border: 1px solid rgba(100, 200, 255, 0.28) !important;
            border-radius: 14px !important;

            backdrop-filter: blur(10px);
        }}

        div[data-baseweb="input"]:focus-within {{
            border-color: #38bdf8 !important;

            box-shadow:
                0 0 20px rgba(56, 189, 248, 0.16);
        }}

        input {{
            color: white !important;
        }}


        /* =====================================================
           ANALYZE BUTTON
        ===================================================== */

        .stButton > button {{
            height: 52px;

            border-radius: 14px;

            border: 1px solid rgba(80, 210, 255, 0.45);

            background: linear-gradient(
                135deg,
                rgba(0, 150, 255, 0.85),
                rgba(70, 80, 220, 0.85)
            );

            color: white;

            font-size: 16px;
            font-weight: 700;

            letter-spacing: 0.4px;

            box-shadow:
                0 8px 25px rgba(0, 120, 255, 0.20);

            transition: all 0.25s ease;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px);

            border-color: #7dd3fc;

            box-shadow:
                0 10px 30px rgba(0, 160, 255, 0.32);
        }}


        /* =====================================================
           IMAGE CONTAINERS
        ===================================================== */

        [data-testid="stImage"] {{
            background: rgba(2, 8, 20, 0.70);

            border-radius: 16px;

            padding: 8px;

            border: 1px solid rgba(100, 200, 255, 0.18);

            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.28);
        }}


        /* =====================================================
           METRICS
        ===================================================== */

        [data-testid="stMetric"] {{
            background: rgba(5, 18, 38, 0.65);

            border: 1px solid rgba(100, 200, 255, 0.16);

            padding: 18px;

            border-radius: 16px;

            backdrop-filter: blur(10px);
        }}

        [data-testid="stMetricValue"] {{
            color: #7dd3fc !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: rgba(220, 240, 255, 0.75) !important;
        }}


        /* =====================================================
           INFO / SUCCESS / WARNING BOXES
        ===================================================== */

        div[data-testid="stAlert"] {{
            border-radius: 14px !important;

            background: rgba(5, 20, 40, 0.68) !important;

            backdrop-filter: blur(10px);
        }}


        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {{
            border: none;

            height: 1px;

            background: linear-gradient(
                90deg,
                transparent,
                rgba(80, 200, 255, 0.35),
                transparent
            );

            margin: 28px 0;
        }}


        /* =====================================================
           CAPTIONS
        ===================================================== */

        .stCaption {{
            color: rgba(210, 235, 250, 0.65) !important;
        }}


        /* =====================================================
           SCROLLBAR
        ===================================================== */

        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: #030814;
        }}

        ::-webkit-scrollbar-thumb {{
            background: rgba(80, 180, 255, 0.35);
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(80, 200, 255, 0.60);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )