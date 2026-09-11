import streamlit as st
import base64
import os

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="SATQUERY-AI",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# HELPER: Load background image as base64 (safe fallback)
# ---------------------------------------------------------
def get_base64_background(image_path: str):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


BG_PATH = os.path.join("assets", "background.png")
bg_base64 = get_base64_background(BG_PATH)

if bg_base64:
    bg_css = f"""
    background-image:
        linear-gradient(180deg, rgba(4,10,14,0.85) 0%, rgba(4,10,14,0.92) 100%),
        url("data:image/png;base64,{bg_base64}");
    """
else:
    bg_css = """
    background: radial-gradient(circle at 20% 20%, #062226 0%, #020a0c 70%);
    """


# ---------------------------------------------------------
# GLOBAL CSS — DARK CYAN / GLASSMORPHISM THEME
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    html, body, [class*="css"] {{
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }}

    .stApp {{
        {bg_css}
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #e6fbff;
    }}

    .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }}

    /* ---------- HEADER ---------- */
    .satq-header {{
        text-align: center;
        margin-bottom: 0.2rem;
    }}

    .satq-logo {{
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: 4px;
        background: linear-gradient(90deg, #00f5d4, #00b4d8, #48cae4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(0, 245, 212, 0.25);
    }}

    .satq-subtitle {{
        font-size: 1rem;
        letter-spacing: 3px;
        color: #7fd8e8;
        text-transform: uppercase;
        margin-top: -8px;
        font-weight: 400;
    }}

    /* ---------- HERO ---------- */
    .satq-hero {{
        text-align: center;
        margin-top: 2.2rem;
        margin-bottom: 2.4rem;
    }}

    .satq-hero-tag {{
        font-size: 0.85rem;
        letter-spacing: 4px;
        color: #4dd0e1;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
        font-weight: 600;
    }}

    .satq-hero-title {{
        font-size: 2.6rem;
        font-weight: 700;
        color: #f0fdff;
        line-height: 1.2;
        text-shadow: 0 0 30px rgba(0, 180, 216, 0.35);
    }}

    /* ---------- GLASS CARD ---------- */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 245, 212, 0.18);
        border-radius: 18px;
        padding: 1.8rem 2rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.6rem;
    }}

    .glass-card h4 {{
        color: #7fe9f5;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }}

    /* ---------- FILE UPLOAD LABELS ---------- */
    .upload-label {{
        color: #8fe4f0;
        font-weight: 600;
        letter-spacing: 1px;
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }}

    /* ---------- TEXT INPUT ---------- */
    .stTextArea textarea, .stTextInput input {{
        background-color: rgba(255,255,255,0.04) !important;
        color: #e6fbff !important;
        border: 1px solid rgba(0, 245, 212, 0.25) !important;
        border-radius: 12px !important;
    }}

    /* ---------- FILE UPLOADER ---------- */
    [data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.03);
        border: 1px dashed rgba(0, 245, 212, 0.3);
        border-radius: 14px;
        padding: 0.6rem;
    }}

    /* ---------- BUTTON ---------- */
    div.stButton > button {{
        width: 100%;
        background: linear-gradient(90deg, #00b4d8, #00f5d4);
        color: #002022;
        font-weight: 700;
        letter-spacing: 1.5px;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        font-size: 1.05rem;
        margin-top: 0.6rem;
        box-shadow: 0 0 25px rgba(0, 245, 212, 0.25);
        transition: all 0.2s ease-in-out;
    }}

    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 35px rgba(0, 245, 212, 0.45);
        color: #001416;
    }}

    /* ---------- FOOTER NOTE ---------- */
    .satq-footnote {{
        text-align: center;
        color: #4a7f8a;
        font-size: 0.8rem;
        margin-top: 1.5rem;
        letter-spacing: 1px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="satq-header">
        <div class="satq-logo">SATQUERY-AI</div>
        <div class="satq-subtitle">Remote Sensing Intelligence</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------
st.markdown(
    """
    <div class="satq-hero">
        <div class="satq-hero-tag">Multimodal Remote Sensing • AI Analysis</div>
        <div class="satq-hero-title">Ask your Satellite.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# QUERY INPUT CARD
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 🛰️ Natural Language Query")
query = st.text_area(
    label="query_input",
    label_visibility="collapsed",
    placeholder="e.g. Analyse vegetation loss between the two images...",
    height=90,
)
st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# IMAGE UPLOAD CARD
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 🖼️ Satellite Imagery Input")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="upload-label">Before Image (Earlier Date)</div>', unsafe_allow_html=True)
    before_file = st.file_uploader(
        "before_uploader",
        type=["png", "jpg", "jpeg", "tif", "tiff"],
        label_visibility="collapsed",
        key="before_uploader",
    )
    if before_file is not None:
        st.image(before_file, use_container_width=True, caption="Before Image Preview")

with col2:
    st.markdown('<div class="upload-label">After Image (Later Date)</div>', unsafe_allow_html=True)
    after_file = st.file_uploader(
        "after_uploader",
        type=["png", "jpg", "jpeg", "tif", "tiff"],
        label_visibility="collapsed",
        key="after_uploader",
    )
    if after_file is not None:
        st.image(after_file, use_container_width=True, caption="After Image Preview")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# ANALYSE BUTTON
# ---------------------------------------------------------
analyse_clicked = st.button("ANALYSE SATELLITE IMAGERY →")

if analyse_clicked:
    if not query or not query.strip():
        st.warning("⚠️ Please enter a natural-language query before analysis.")
    elif before_file is None or after_file is None:
        st.warning("⚠️ Please upload both the Before and After satellite images.")
    else:
        st.session_state["satquery_data"] = {
            "query": query.strip(),
            "before_bytes": before_file.getvalue(),
            "after_bytes": after_file.getvalue(),
        }
        st.switch_page("pages/analysis.py")


# ---------------------------------------------------------
# FOOTNOTE
# ---------------------------------------------------------
st.markdown(
    """
    <div class="satq-footnote">
        SATQUERY-AI Prototype • Smart India Hackathon • RGB-based Temporal Change Detection
    </div>
    """,
    unsafe_allow_html=True,
)