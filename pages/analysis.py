import streamlit as st
import numpy as np
from PIL import Image
import io

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="SATQUERY-AI | Analysis",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# GLOBAL CSS — DARK CYAN / GLASSMORPHISM THEME
# ---------------------------------------------------------
st.markdown(
    """
    <style>

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #062226 0%, #020a0c 65%);
        color: #e6fbff;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }

    .satq-header {
        text-align: center;
        margin-bottom: 1.6rem;
    }

    .satq-logo {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 4px;
        background: linear-gradient(90deg, #00f5d4, #00b4d8, #48cae4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(0, 245, 212, 0.25);
    }

    .satq-subtitle {
        font-size: 0.9rem;
        letter-spacing: 3px;
        color: #7fd8e8;
        text-transform: uppercase;
        margin-top: -6px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 245, 212, 0.18);
        border-radius: 18px;
        padding: 1.6rem 1.8rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.4rem;
    }

    .glass-card h4 {
        color: #7fe9f5;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }

    .metric-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(0, 245, 212, 0.15);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        text-align: center;
        margin-bottom: 0.6rem;
    }

    .metric-label {
        font-size: 0.75rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #7fd8e8;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f0fdff;
    }

    .finding-box {
        background: rgba(0, 245, 212, 0.07);
        border-left: 4px solid #00f5d4;
        border-radius: 10px;
        padding: 1rem 1.3rem;
        color: #e6fbff;
        font-size: 1.02rem;
        line-height: 1.55;
    }

    .query-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(0, 245, 212, 0.15);
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        color: #bdeef5;
        font-style: italic;
    }

    .tech-note {
        background: rgba(255, 190, 0, 0.06);
        border-left: 4px solid #ffb703;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        color: #ffe0a3;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-top: 1rem;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #00b4d8, #00f5d4);
        color: #002022;
        font-weight: 700;
        letter-spacing: 1.5px;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 1.2rem;
        font-size: 1.0rem;
        margin-top: 0.6rem;
        box-shadow: 0 0 25px rgba(0, 245, 212, 0.25);
        transition: all 0.2s ease-in-out;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 35px rgba(0, 245, 212, 0.45);
        color: #001416;
    }

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
        <div class="satq-subtitle">Change Analysis Report</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# GUARD: NO DATA IN SESSION STATE
# ---------------------------------------------------------
if "satquery_data" not in st.session_state or st.session_state["satquery_data"] is None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.warning(
        "⚠️ No analysis data found. Please go back to the home page, "
        "enter a query, and upload both satellite images."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("← Back to Home"):
        st.switch_page("app.py")

    st.stop()


# ---------------------------------------------------------
# LOAD DATA FROM SESSION STATE
# ---------------------------------------------------------
data = st.session_state["satquery_data"]
query_text = data.get("query", "")
before_bytes = data.get("before_bytes")
after_bytes = data.get("after_bytes")

try:
    before_img = Image.open(io.BytesIO(before_bytes)).convert("RGB")
    after_img = Image.open(io.BytesIO(after_bytes)).convert("RGB")
except Exception as e:
    st.error(f"❌ Could not open one or both images. Error: {e}")
    if st.button("← Back to Home"):
        st.switch_page("app.py")
    st.stop()


# ---------------------------------------------------------
# ANALYSIS FUNCTIONS
# ---------------------------------------------------------
def detect_target(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["vegetation", "forest", "tree", "green", "crop", "farm", "plant"]):
        return "Vegetation"
    if any(k in q for k in ["water", "river", "lake", "flood", "sea", "ocean", "pond", "reservoir"]):
        return "Water Body"
    if any(k in q for k in ["urban", "built", "building", "construction", "infrastructure", "road", "city"]):
        return "Built-up Area"
    if any(k in q for k in ["land", "soil", "terrain", "cover", "surface"]):
        return "Land Cover"
    return "General Scene"


def run_change_detection(before_img: Image.Image, after_img: Image.Image, size=(512, 512)):
    before_resized = before_img.resize(size)
    after_resized = after_img.resize(size)

    before_arr = np.array(before_resized).astype(np.float32)
    after_arr = np.array(after_resized).astype(np.float32)

    diff = np.abs(after_arr - before_arr)
    diff_gray = np.mean(diff, axis=2)  # 0 - 255 grayscale difference

    threshold = 30.0
    change_mask = diff_gray > threshold

    total_pixels = change_mask.size
    changed_pixels = int(np.sum(change_mask))
    affected_area_pct = round((changed_pixels / total_pixels) * 100, 2)

    change_intensity_pct = round((np.mean(diff_gray) / 255.0) * 100, 2)

    change_map_img = Image.fromarray(diff_gray.astype(np.uint8))

    if changed_pixels > 0:
        before_mean = float(np.mean(before_arr[change_mask]))
        after_mean = float(np.mean(after_arr[change_mask]))
    else:
        before_mean = float(np.mean(before_arr))
        after_mean = float(np.mean(after_arr))

    delta = after_mean - before_mean
    if delta > 5:
        direction = "Increase (brighter / denser signal in after image)"
    elif delta < -5:
        direction = "Decrease (darker / reduced signal in after image)"
    else:
        direction = "Stable / Mixed (no dominant directional shift)"

    if change_intensity_pct < 10:
        intensity_label = "Low"
    elif change_intensity_pct < 30:
        intensity_label = "Moderate"
    else:
        intensity_label = "High"

    return {
        "change_map_img": change_map_img,
        "affected_area_pct": affected_area_pct,
        "change_intensity_pct": change_intensity_pct,
        "intensity_label": intensity_label,
        "direction": direction,
    }


def generate_finding(target: str, result: dict, query: str) -> str:
    return (
        f"Based on the temporal RGB comparison, the region associated with "
        f"**{target}** shows a **{result['intensity_label'].lower()} intensity** change "
        f"({result['change_intensity_pct']}%), affecting approximately "
        f"**{result['affected_area_pct']}%** of the analyzed scene. "
        f"The dominant change pattern observed is: **{result['direction']}**. "
        f"This is consistent with the query: \"{query}\"."
    )


# ---------------------------------------------------------
# RUN ANALYSIS
# ---------------------------------------------------------
target = detect_target(query_text)
result = run_change_detection(before_img, after_img)
finding = generate_finding(target, result, query_text)


# ---------------------------------------------------------
# IMAGE DISPLAY
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 🖼️ Imagery Comparison")

img_col1, img_col2, img_col3 = st.columns(3)

with img_col1:
    st.image(before_img, use_container_width=True, caption="Before Image")

with img_col2:
    st.image(after_img, use_container_width=True, caption="After Image")

with img_col3:
    st.image(result["change_map_img"], use_container_width=True, caption="Detected Change Map")

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 📊 Analysis Metrics")

m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Analysis Target</div>
            <div class="metric-value">{target}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m_col2:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Change Direction</div>
            <div class="metric-value" style="font-size:1.05rem;">{result['direction'].split(' (')[0]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m_col3:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Affected Area</div>
            <div class="metric-value">{result['affected_area_pct']}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m_col4:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Change Intensity</div>
            <div class="metric-value">{result['change_intensity_pct']}% ({result['intensity_label']})</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# AI FINDING
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 🤖 AI Finding")
st.markdown(f'<div class="finding-box">{finding}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# ORIGINAL QUERY
# ---------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### 💬 Original User Query")
st.markdown(f'<div class="query-box">"{query_text}"</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="tech-note">
        ⚠️ <b>Technical Note:</b> This prototype performs RGB image-based pixel-level
        temporal change detection for demonstration purposes. Accurate vegetation (NDVI),
        water (NDWI), or built-up area (NDBI) analysis requires appropriate multispectral
        or hyperspectral satellite bands (e.g. NIR, SWIR), which are not derivable from
        standard RGB imagery alone.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# NEW ANALYSIS BUTTON
# ---------------------------------------------------------
if st.button("🔄 Start New Analysis"):
    st.session_state["satquery_data"] = None
    st.switch_page("app.py")