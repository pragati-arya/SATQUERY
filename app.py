import streamlit as st
from PIL import Image

from modules.query import understand_query, get_intent_name
from modules.analysis import (
    run_analysis,
    create_overlay,
    get_change_level
)
from modules.ui import apply_space_background


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SATQUERY AI",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# APPLY SPACE BACKGROUND + CSS
# =========================================================

apply_space_background()


# =========================================================
# HEADER
# =========================================================

st.title("🛰️ SATQUERY AI")

st.markdown(
    "**Interactive Vision-Language Assistant for "
    "Multimodal Remote Sensing Analysis**"
)

st.caption("● AI ANALYSIS SYSTEM ONLINE")


# =========================================================
# SATELLITE IMAGE ANALYSIS
# =========================================================

st.divider()

st.header("🛰️ Satellite Image Analysis")

st.write(
    "Upload two temporal images of the same area "
    "to identify candidate changes."
)


# =========================================================
# IMAGE UPLOAD
# =========================================================

col1, col2 = st.columns(2, gap="large")


with col1:

    st.subheader("🕐 Before Image")

    before_file = st.file_uploader(
        "Upload earlier satellite image",
        type=["jpg", "jpeg", "png"],
        key="before_upload"
    )

    if before_file is not None:

        before_preview = Image.open(
            before_file
        ).convert("RGB")

        st.image(
            before_preview,
            caption="Earlier Image",
            use_container_width=True
        )


with col2:

    st.subheader("🕐 After Image")

    after_file = st.file_uploader(
        "Upload later satellite image",
        type=["jpg", "jpeg", "png"],
        key="after_upload"
    )

    if after_file is not None:

        after_preview = Image.open(
            after_file
        ).convert("RGB")

        st.image(
            after_preview,
            caption="Later Image",
            use_container_width=True
        )


# =========================================================
# QUERY SECTION
# =========================================================

st.divider()

st.header("💬 Ask SATQUERY")

st.write(
    "Ask your question naturally in English or Hinglish."
)


query = st.text_input(
    "Natural Language Query",
    placeholder="Example: Is area mein vegetation badhi hai?",
    key="query_input"
)


st.caption(
    "Try: Show vegetation increase • "
    "Paani ka area kam hua hai? • "
    "Yahan construction badha hai? • "
    "Show major changes"
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 ANALYZE SATELLITE DATA",
    use_container_width=True
):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if before_file is None:

        st.warning(
            "⚠️ Please upload the Before image."
        )

        st.stop()


    if after_file is None:

        st.warning(
            "⚠️ Please upload the After image."
        )

        st.stop()


    if not query.strip():

        st.warning(
            "⚠️ Please enter a natural-language query."
        )

        st.stop()


    # -----------------------------------------------------
    # LOAD IMAGES
    # -----------------------------------------------------

    before = Image.open(
        before_file
    ).convert("RGB")

    after = Image.open(
        after_file
    ).convert("RGB")


    # -----------------------------------------------------
    # IMAGE SIZE ALIGNMENT
    # -----------------------------------------------------

    if after.size != before.size:

        after = after.resize(
            before.size,
            Image.Resampling.BILINEAR
        )


    # -----------------------------------------------------
    # QUERY UNDERSTANDING
    # -----------------------------------------------------

    intent = understand_query(query)


    # -----------------------------------------------------
    # RUN ANALYSIS
    # -----------------------------------------------------

    with st.spinner(
        "🛰️ SATQUERY is analysing the satellite images..."
    ):

        result = run_analysis(
            before,
            after,
            intent
        )


    # =====================================================
    # QUERY UNDERSTANDING RESULT
    # =====================================================

    st.divider()

    st.header("🧠 Query Understanding")

    st.info(
        f"**Detected Analysis:** "
        f"{get_intent_name(intent)}"
    )

    st.write(
        f"**User Query:** {query}"
    )


    # =====================================================
    # CHANGE DETECTION RESULT
    # =====================================================

    st.divider()

    st.header("🗺️ Change Detection Result")


    # -----------------------------------------------------
    # CREATE RESULT OVERLAY
    # -----------------------------------------------------

    overlay_image = create_overlay(
        after,
        result["mask"],
        result["color"]
    )


    # -----------------------------------------------------
    # DISPLAY IMAGES
    # -----------------------------------------------------

    result_col1, result_col2, result_col3 = st.columns(
        3,
        gap="medium"
    )


    with result_col1:

        st.subheader("🕐 Before")

        st.image(
            before,
            use_container_width=True
        )


    with result_col2:

        st.subheader("🕐 After")

        st.image(
            after,
            use_container_width=True
        )


    with result_col3:

        st.subheader("🧠 SATQUERY Result")

        st.image(
            overlay_image,
            caption=result["name"],
            use_container_width=True
        )


    # =====================================================
    # MAP LEGEND
    # =====================================================

    st.subheader("🗺️ Map Legend")


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
            "🔴 Red = Candidate built-up/construction change"
        )


    else:

        st.error(
            "🔴 Red = Strong RGB temporal difference"
        )


    # =====================================================
    # ANALYSIS SUMMARY
    # =====================================================

    st.divider()

    st.header("📊 Analysis Summary")


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

    st.header("🤖 SATQUERY Explanation")

    st.write(
        result["explanation"]
    )


    # =====================================================
    # EVIDENCE
    # =====================================================

    st.divider()

    st.header("🔎 Evidence")


    evidence_col1, evidence_col2 = st.columns(2)


    with evidence_col1:

        st.metric(
            "Detected Region",
            f"{result['pct']:.2f}%"
        )

        st.caption(
            "Percentage of analysed pixels flagged "
            "as candidate change."
        )


    with evidence_col2:

        st.metric(
            "Change Assessment",
            get_change_level(
                result["pct"]
            )
        )

        st.caption(
            "Based on the detected change extent."
        )


    # =====================================================
    # PROTOTYPE LIMITATIONS
    # =====================================================

    st.divider()

    st.header("⚠️ Prototype Notes")

    st.caption(
        "This prototype currently uses RGB computer vision. "
        "For reliable satellite change detection, the final "
        "system should incorporate geospatial alignment, "
        "multispectral bands/NDVI, cloud masking, SAR where "
        "appropriate, and land-cover/building segmentation. "
        "Highlighted regions represent candidate changes, "
        "not confirmed construction."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🛰️ SATQUERY AI  •  Remote Sensing Intelligence  •  SIH 2026"
)