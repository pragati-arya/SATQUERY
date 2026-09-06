import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="SATQUERY AI",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ SATQUERY AI")
st.write("Natural Language Satellite Image Analysis Prototype")
st.caption("Ask questions about changes in satellite imagery.")

# --------------------------------------------------
# QUERY UNDERSTANDING
# --------------------------------------------------

def understand_query(query):
    q = query.lower()

    if any(x in q for x in [
        "vegetation", "greenery", "forest",
        "crop", "plant", "ndvi", "green"
    ]):
        return "Vegetation Analysis"

    if any(x in q for x in [
        "water", "lake", "river",
        "pond", "waterbody", "water body"
    ]):
        return "Water-body Change Analysis"

    if any(x in q for x in [
        "building", "built-up", "built up",
        "construction", "urban", "city",
        "development"
    ]):
        return "Built-up Area Analysis"

    if any(x in q for x in [
        "change", "changed", "difference",
        "compare", "comparison"
    ]):
        return "Temporal Change Detection"

    return "General Remote Sensing Analysis"


# --------------------------------------------------
# ANALYSIS FUNCTIONS
# --------------------------------------------------

def vegetation_analysis(image):
    """
    RGB-based vegetation approximation.

    Uses Excess Green Index:
    2G - R - B
    """

    arr = np.array(image).astype(float)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    excess_green = (2 * g - r - b)

    threshold = np.percentile(excess_green, 65)

    mask = excess_green > threshold

    return mask


def water_analysis(image):
    """
    Simple RGB water approximation.

    Water often has relatively stronger blue
    response than red in RGB imagery.
    """

    arr = np.array(image).astype(float)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    water_score = b - r

    threshold = np.percentile(water_score, 70)

    mask = water_score > threshold

    return mask


def builtup_analysis(image):
    """
    Simple RGB built-up approximation.

    Built-up surfaces tend to have relatively
    low vegetation signal and moderate brightness.
    """

    arr = np.array(image).astype(float)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    brightness = (r + g + b) / 3

    vegetation_signal = (2 * g - r - b)

    mask = (
        (brightness > np.percentile(brightness, 35))
        &
        (vegetation_signal < np.percentile(
            vegetation_signal, 45
        ))
    )

    return mask


def change_detection(before, after):
    """
    RGB pixel-by-pixel temporal change detection.
    """

    before_arr = np.array(before).astype(float)
    after_arr = np.array(after).astype(float)

    difference = np.abs(
        before_arr - after_arr
    )

    change_score = np.mean(
        difference,
        axis=2
    )

    threshold = 30

    mask = change_score > threshold

    return mask, threshold


# --------------------------------------------------
# UPLOAD
# --------------------------------------------------

st.divider()

st.subheader("🛰️ Upload Satellite Images")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Before Image")

    before_file = st.file_uploader(
        "Upload earlier satellite image",
        type=["jpg", "jpeg", "png"],
        key="before"
    )

with col2:
    st.markdown("### After Image")

    after_file = st.file_uploader(
        "Upload later satellite image",
        type=["jpg", "jpeg", "png"],
        key="after"
    )


# --------------------------------------------------
# QUERY
# --------------------------------------------------

st.divider()

st.subheader("💬 Ask SATQUERY")

query = st.text_input(
    "Enter your query",
    placeholder="Example: Show vegetation changes"
)

st.caption(
    "Examples: vegetation changes • water changes • "
    "new buildings • major changes"
)


# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

if st.button(
    "🔍 Analyze",
    use_container_width=True
):

    if before_file is None or after_file is None:

        st.warning(
            "Please upload both Before and After images."
        )

        st.stop()

    if not query.strip():

        st.warning(
            "Please enter a query."
        )

        st.stop()

    # --------------------------------------------------
    # LOAD IMAGES
    # --------------------------------------------------

    before = Image.open(
        before_file
    ).convert("RGB")

    after = Image.open(
        after_file
    ).convert("RGB")

    after = after.resize(
        before.size
    )

    # --------------------------------------------------
    # UNDERSTAND QUERY
    # --------------------------------------------------

    intent = understand_query(query)

    st.divider()

    st.subheader("🧠 Query Understanding")

    st.info(
        f"**Detected Analysis:** {intent}"
    )

    # --------------------------------------------------
    # SELECT ANALYSIS
    # --------------------------------------------------

    if intent == "Vegetation Analysis":

        before_mask = vegetation_analysis(
            before
        )

        after_mask = vegetation_analysis(
            after
        )

        # New / lost vegetation
        changed_mask = before_mask != after_mask

        result_title = "🌳 Vegetation Change Map"

        explanation = (
            "SATQUERY identified vegetation-related "
            "features using an RGB-based vegetation "
            "index approximation. The highlighted regions "
            "represent areas where the vegetation signal "
            "changed between the two images."
        )

        threshold_value = "65th percentile"

    elif intent == "Water-body Change Analysis":

        before_mask = water_analysis(
            before
        )

        after_mask = water_analysis(
            after
        )

        changed_mask = before_mask != after_mask

        result_title = "💧 Water-body Change Map"

        explanation = (
            "SATQUERY identified likely water regions "
            "using RGB spectral relationships. The "
            "highlighted regions indicate changes in "
            "the detected water signal."
        )

        threshold_value = "70th percentile"

    elif intent == "Built-up Area Analysis":

        before_mask = builtup_analysis(
            before
        )

        after_mask = builtup_analysis(
            after
        )

        changed_mask = before_mask != after_mask

        result_title = "🏙️ Built-up Area Change Map"

        explanation = (
            "SATQUERY identified likely built-up surfaces "
            "using brightness and vegetation-signal "
            "characteristics. Highlighted regions indicate "
            "areas where the built-up signal changed."
        )

        threshold_value = "Adaptive percentile"

    else:

        changed_mask, threshold = change_detection(
            before,
            after
        )

        result_title = "🔄 Temporal Change Map"

        explanation = (
            "SATQUERY compared the Before and After "
            "images pixel-by-pixel and identified regions "
            "with significant visual differences."
        )

        threshold_value = str(threshold)

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    st.divider()

    st.subheader(result_title)

    c1, c2, c3 = st.columns(3)

    with c1:

        st.image(
            before,
            caption="Before",
            use_container_width=True
        )

    with c2:

        st.image(
            after,
            caption="After",
            use_container_width=True
        )

    with c3:

        fig, ax = plt.subplots()

        ax.imshow(
            changed_mask,
            cmap="Reds"
        )

        ax.set_title(
            "Detected Changes"
        )

        ax.axis("off")

        st.pyplot(fig)

        plt.close(fig)

    # --------------------------------------------------
    # STATISTICS
    # --------------------------------------------------

    total_pixels = changed_mask.size

    changed_pixels = np.sum(
        changed_mask
    )

    changed_percentage = (
        changed_pixels /
        total_pixels
    ) * 100

    st.divider()

    st.subheader("📊 Analysis Summary")

    s1, s2, s3 = st.columns(3)

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
            "Analysis Threshold",
            threshold_value
        )

    # --------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------

    st.subheader("🔎 SATQUERY Explanation")

    st.write(explanation)

    st.caption(
        "Prototype limitation: this version uses "
        "RGB imagery. True NDVI and multispectral "
        "analysis require multispectral satellite bands."
    )