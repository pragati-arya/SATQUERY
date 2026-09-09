# =========================================================
# SATQUERY-AI
# MAIN APPLICATION
# =========================================================

import streamlit as st

from PIL import Image

from modules.query import (
    understand_query,
    get_intent_name
)

from modules.analysis import (
    run_analysis,
    create_overlay,
    get_change_level
)

from modules.ui import (
    apply_space_background
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="SATQUERY AI",

    page_icon="🛰️",

    layout="wide"
)


# =========================================================
# APPLY BACKGROUND
# =========================================================

apply_space_background()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🛰️ SATQUERY AI
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Interactive Vision-Language Assistant
        for Satellite Image Analysis
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

st.divider()


# =========================================================
# UPLOAD IMAGES
# =========================================================

st.subheader(
    "🛰️ Upload Satellite Images"
)

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        "### Before Image"
    )

    before_file = st.file_uploader(

        "Upload earlier satellite image",

        type=[
            "jpg",
            "jpeg",
            "png"
        ],

        key="before_upload"
    )


with col2:

    st.markdown(
        "### After Image"
    )

    after_file = st.file_uploader(

        "Upload later satellite image",

        type=[
            "jpg",
            "jpeg",
            "png"
        ],

        key="after_upload"
    )


# =========================================================
# QUERY
# =========================================================

st.divider()

st.subheader(
    "💬 Ask SATQUERY"
)

st.caption(
    "Ask your question in English or Hinglish"
)


query = st.text_input(

    "Enter your query",

    placeholder=(
        "Example: Is area mein "
        "vegetation badhi hai?"
    ),

    key="query_input"
)


st.caption(
    "Examples: "
    "Show vegetation increase • "
    "Paani ka area kam hua hai? • "
    "Yahan construction badha hai? • "
    "Show major changes"
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze",
    use_container_width=True
):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if before_file is None:

        st.warning(
            "Please upload the Before image."
        )

        st.stop()


    if after_file is None:

        st.warning(
            "Please upload the After image."
        )

        st.stop()


    if not query.strip():

        st.warning(
            "Please enter a query."
        )

        st.stop()


    # -----------------------------------------------------
    # LOAD BEFORE IMAGE
    # -----------------------------------------------------

    before = Image.open(
        before_file
    ).convert("RGB")


    # -----------------------------------------------------
    # LOAD AFTER IMAGE
    # -----------------------------------------------------

    after = Image.open(
        after_file
    ).convert("RGB")


    # -----------------------------------------------------
    # MATCH IMAGE SIZE
    # -----------------------------------------------------

    after = after.resize(
        before.size,
        Image.Resampling.BILINEAR
    )


    # -----------------------------------------------------
    # UNDERSTAND QUERY
    # -----------------------------------------------------

    intent = understand_query(
        query
    )


    # -----------------------------------------------------
    # RUN ANALYSIS
    # -----------------------------------------------------

    with st.spinner(
        "🛰️ SATQUERY is analysing the images..."
    ):

        result = run_analysis(

            before,

            after,

            intent
        )


    # =====================================================
    # QUERY UNDERSTANDING
    # =====================================================

    st.divider()

    st.subheader(
        "🧠 Query Understanding"
    )

    st.info(
        f"**Detected analysis:** "
        f"{get_intent_name(intent)}"
    )

    st.write(
        f"**User query:** {query}"
    )


    # =====================================================
    # CHANGE DETECTION RESULT
    # =====================================================

    st.divider()

    st.subheader(
        "🗺️ Change Detection Result"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.image(

            before,

            caption="Before",

            use_container_width=True

        )


    with col2:

        st.image(

            after,

            caption="After",

            use_container_width=True

        )


    with col3:

        overlay_image = create_overlay(

            after,

            result["mask"],

            result["color"]

        )

        st.image(

            overlay_image,

            caption=result["name"],

            use_container_width=True

        )


    # =====================================================
    # LEGEND
    # =====================================================

    st.markdown(
        "### 🗺️ Map Legend"
    )


    if intent == "vegetation_increase":

        st.success(
            "🟢 Green = Candidate vegetation increase"
        )


    elif intent == "vegetation_decrease":

        st.warning(
            "🟠 Orange = Candidate vegetation decrease"
        )


    elif intent in [
        "water_change",
        "water_decrease"
    ]:

        st.info(
            "🔵 Blue = Candidate water-related change"
        )


    elif intent == "construction_increase":

        st.error(
            "🔴 Red = Candidate built-up/"
            "construction change"
        )


    else:

        st.error(
            "🔴 Red = Strong RGB temporal difference"
        )


    # =====================================================
    # ANALYSIS SUMMARY
    # =====================================================

    st.divider()

    st.subheader(
        "📊 Analysis Summary"
    )


    s1, s2, s3, s4 = st.columns(4)


    with s1:

        st.metric(
            "Changed Area",
            f"{result['pct']:.2f}%"
        )


    with s2:

        st.metric(
            "Pixels Analysed",
            f"{result['total']:,}"
        )


    with s3:

        st.metric(
            "Change Level",
            get_change_level(
                result["pct"]
            )
        )


    with s4:

        st.metric(
            "Adaptive Threshold",
            f"{result['threshold']:.3f}"
        )


    # =====================================================
    # EXPLANATION
    # =====================================================

    st.divider()

    st.subheader(
        "🤖 SATQUERY Explanation"
    )

    st.write(
        result["explanation"]
    )


    # =====================================================
    # LIMITATIONS
    # =====================================================

    st.divider()

    st.subheader(
        "⚠️ Prototype Limitations"
    )

    st.caption(
        "This prototype uses RGB computer vision. "
        "Reliable satellite change detection should use "
        "geospatial alignment, multispectral bands/NDVI, "
        "cloud masking, SAR where appropriate, and "
        "land-cover/building segmentation. "
        "Highlighted regions are candidate changes, "
        "not confirmed construction."
    )