import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SATQUERY AI",
    page_icon="🛰️",
    layout="wide"
)


# ============================================================
# QUERY UNDERSTANDING
# ============================================================

def understand_query(query):
    q = query.lower()

    vegetation_words = [
        "vegetation",
        "greenery",
        "forest",
        "crop",
        "plant",
        "ndvi",
        "green"
    ]

    water_words = [
        "water",
        "lake",
        "river",
        "pond",
        "waterbody",
        "water body"
    ]

    builtup_words = [
        "building",
        "built-up",
        "built up",
        "construction",
        "urban",
        "city",
        "development"
    ]

    change_words = [
        "change",
        "changed",
        "difference",
        "compare",
        "comparison"
    ]

    if any(word in q for word in vegetation_words):
        return "Vegetation Analysis"

    elif any(word in q for word in water_words):
        return "Water-body Change Analysis"

    elif any(word in q for word in builtup_words):
        return "Built-up Area Analysis"

    elif any(word in q for word in change_words):
        return "Temporal Change Detection"

    else:
        return "General Remote Sensing Analysis"


# ============================================================
# VEGETATION ANALYSIS
# ============================================================

def vegetation_analysis(image):

    arr = np.array(image).astype(float)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # RGB-based vegetation approximation
    excess_green = (2 * g - r - b)

    threshold = np.percentile(
        excess_green,
        65
    )

    mask = excess_green > threshold

    return mask


# ============================================================
# WATER ANALYSIS
# ============================================================

def water_analysis(image):

    arr = np.array(image).astype(float)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    # Simple RGB water approximation
    water_score = b - r

    threshold = np.percentile(
        water_score,
        70
    )

    mask = water_score > threshold

    return mask


# ============================================================
# BUILT-UP ANALYSIS
# ============================================================

def builtup_analysis(image):

    arr = np.array(image).astype(float)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    brightness = (
        r + g + b
    ) / 3

    vegetation_signal = (
        2 * g - r - b
    )

    brightness_threshold = np.percentile(
        brightness,
        35
    )

    vegetation_threshold = np.percentile(
        vegetation_signal,
        45
    )

    mask = (
        (brightness > brightness_threshold)
        &
        (vegetation_signal < vegetation_threshold)
    )

    return mask


# ============================================================
# GENERAL CHANGE DETECTION
# ============================================================

def change_detection(before, after):

    before_array = np.array(
        before
    ).astype(float)

    after_array = np.array(
        after
    ).astype(float)

    difference = np.abs(
        before_array - after_array
    )

    change_score = np.mean(
        difference,
        axis=2
    )

    threshold = 30

    mask = change_score > threshold

    return mask, threshold


# ============================================================
# CHANGE LEVEL
# ============================================================

def get_change_level(percentage):

    if percentage < 10:
        return "Low Change"

    elif percentage < 30:
        return "Moderate Change"

    elif percentage < 60:
        return "High Change"

    else:
        return "Very High Change"


# ============================================================
# HEADER
# ============================================================

st.title("🛰️ SATQUERY AI")

st.subheader(
    "Interactive Vision-Language Assistant for "
    "Remote Sensing Image Analysis"
)

st.write(
    "Ask questions about satellite imagery using "
    "natural language."
)

st.divider()


# ============================================================
# IMAGE UPLOAD
# ============================================================

st.subheader("🛰️ Upload Satellite Images")

col1, col2 = st.columns(2)


with col1:

    st.markdown("### Before Image")

    before_file = st.file_uploader(
        "Upload earlier satellite image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="before"
    )


with col2:

    st.markdown("### After Image")

    after_file = st.file_uploader(
        "Upload later satellite image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="after"
    )


# ============================================================
# QUERY INPUT
# ============================================================

st.divider()

st.subheader("💬 Ask SATQUERY")

query = st.text_input(
    "Enter your query",
    placeholder="Example: Show vegetation changes"
)


st.markdown("**Try asking:**")

st.caption(
    "🌳 Show vegetation changes"
)

st.caption(
    "💧 Show water-body changes"
)

st.caption(
    "🏙️ Find newly built-up areas"
)

st.caption(
    "🔄 Show major changes between the images"
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🔍 Analyze",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # LOAD IMAGES
    # --------------------------------------------------------

    before = Image.open(
        before_file
    ).convert("RGB")

    after = Image.open(
        after_file
    ).convert("RGB")


    # Make image dimensions identical
    after = after.resize(
        before.size
    )


    # --------------------------------------------------------
    # QUERY UNDERSTANDING
    # --------------------------------------------------------

    intent = understand_query(
        query
    )


    st.divider()

    st.subheader(
        "🧠 Query Understanding"
    )


    q1, q2 = st.columns(2)


    with q1:

        st.metric(
            "Detected Intent",
            intent
        )


    with q2:

        st.metric(
            "Input Type",
            "Bi-temporal Images"
        )


    st.info(
        f"SATQUERY interpreted your query as "
        f"**{intent}**."
    )


    # --------------------------------------------------------
    # SELECT ANALYSIS
    # --------------------------------------------------------

    if intent == "Vegetation Analysis":

        before_mask = vegetation_analysis(
            before
        )

        after_mask = vegetation_analysis(
            after
        )

        changed_mask = (
            before_mask != after_mask
        )

        result_title = (
            "🌳 Vegetation Change Analysis"
        )

        explanation = (
            "SATQUERY detected vegetation-related "
            "regions using an RGB-based vegetation "
            "signal. The highlighted areas indicate "
            "where the vegetation signal differs "
            "between the two observations."
        )

        threshold_value = (
            "65th percentile"
        )


    elif intent == "Water-body Change Analysis":

        before_mask = water_analysis(
            before
        )

        after_mask = water_analysis(
            after
        )

        changed_mask = (
            before_mask != after_mask
        )

        result_title = (
            "💧 Water-body Change Analysis"
        )

        explanation = (
            "SATQUERY identified likely water regions "
            "using RGB spectral relationships. "
            "Highlighted areas represent changes "
            "in the detected water signal."
        )

        threshold_value = (
            "70th percentile"
        )


    elif intent == "Built-up Area Analysis":

        before_mask = builtup_analysis(
            before
        )

        after_mask = builtup_analysis(
            after
        )

        changed_mask = (
            before_mask != after_mask
        )

        result_title = (
            "🏙️ Built-up Area Change Analysis"
        )

        explanation = (
            "SATQUERY identified likely built-up "
            "surfaces using brightness and vegetation "
            "signal characteristics. Highlighted "
            "regions indicate areas where this signal "
            "changed."
        )

        threshold_value = (
            "Adaptive percentile"
        )


    else:

        changed_mask, threshold = change_detection(
            before,
            after
        )

        result_title = (
            "🔄 Temporal Change Detection"
        )

        explanation = (
            "SATQUERY compared the Before and After "
            "images pixel-by-pixel and identified "
            "regions with significant visual "
            "differences."
        )

        threshold_value = str(
            threshold
        )


    # ========================================================
    # RESULTS
    # ========================================================

    st.divider()

    st.subheader(
        result_title
    )


    c1, c2, c3 = st.columns(3)


    # --------------------------------------------------------
    # BEFORE
    # --------------------------------------------------------

    with c1:

        st.image(
            before,
            caption="Before",
            use_container_width=True
        )


    # --------------------------------------------------------
    # AFTER
    # --------------------------------------------------------

    with c2:

        st.image(
            after,
            caption="After",
            use_container_width=True
        )


    # --------------------------------------------------------
    # CHANGE OVERLAY
    # --------------------------------------------------------

    with c3:

        after_array = np.array(
            after
        ).copy()


        # Slightly darken the image
        overlay = (
            after_array.astype(float)
            * 0.70
        )

        overlay = np.clip(
            overlay,
            0,
            255
        ).astype(np.uint8)


        # Highlight detected changes
        overlay[changed_mask] = [
            255,
            0,
            0
        ]


        fig, ax = plt.subplots(
            figsize=(5, 4)
        )


        ax.imshow(
            overlay
        )


        ax.set_title(
            "Detected Changes"
        )


        ax.axis("off")


        st.pyplot(
            fig,
            use_container_width=True
        )


        plt.close(fig)


    # ========================================================
    # LEGEND
    # ========================================================

    st.markdown(
        """
        **Map Legend**

        🔴 **Red = Detected change**

        ⚪ **Normal area = No significant detected change**
        """
    )


    # ========================================================
    # STATISTICS
    # ========================================================

    total_pixels = changed_mask.size

    changed_pixels = np.sum(
        changed_mask
    )


    changed_percentage = (
        changed_pixels
        / total_pixels
    ) * 100


    change_level = get_change_level(
        changed_percentage
    )


    st.divider()

    st.subheader(
        "📊 Analysis Summary"
    )


    s1, s2, s3, s4 = st.columns(4)


    with s1:

        st.metric(
            "Changed Area",
            f"{changed_percentage:.2f}%"
        )


    with s2:

        st.metric(
            "Pixels Analysed",
            f"{total_pixels:,}"
        )


    with s3:

        st.metric(
            "Change Level",
            change_level
        )


    with s4:

        st.metric(
            "Threshold",
            threshold_value
        )


    # ========================================================
    # QUERY RESULT
    # ========================================================

    st.divider()

    st.subheader(
        "🔎 SATQUERY Explanation"
    )


    st.write(
        explanation
    )


    st.info(
        f"**Query:** {query}"
    )


    # ========================================================
    # PROTOTYPE DISCLAIMER
    # ========================================================

    st.caption(
        "Prototype limitation: This version uses "
        "RGB imagery and lightweight computer-vision "
        "methods. True multispectral NDVI, SAR fusion, "
        "geospatial alignment and advanced vision-language "
        "models are planned for subsequent versions."
    )