import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SATQUERY AI",
    page_icon="🛰️",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("🛰️ SATQUERY AI")
st.write(
    "Interactive Vision-Language Assistant for Remote Sensing Image Analysis"
)

st.divider()

# -----------------------------
# IMAGE UPLOAD
# -----------------------------
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

# -----------------------------
# QUERY
# -----------------------------
st.divider()

st.subheader("💬 Ask SATQUERY")

query = st.text_input(
    "Enter your query",
    placeholder="Example: Show areas where significant changes occurred..."
)

# -----------------------------
# ANALYSIS
# -----------------------------
if st.button("🔍 Analyze", use_container_width=True):

    if before_file is None or after_file is None:
        st.warning("Please upload both Before and After images.")

    elif not query.strip():
        st.warning("Please enter a query.")

    else:

        before = Image.open(before_file).convert("RGB")
        after = Image.open(after_file).convert("RGB")

        # Resize after image to match before image
        after = after.resize(before.size)

        before_array = np.array(before).astype(float)
        after_array = np.array(after).astype(float)

        # Calculate pixel difference
        difference = np.abs(before_array - after_array)

        # Convert RGB difference into one value per pixel
        change_score = np.mean(difference, axis=2)

        # Threshold for significant change
        threshold = 30

        change_mask = change_score > threshold

        # Calculate percentage of changed pixels
        changed_pixels = np.sum(change_mask)
        total_pixels = change_mask.size

        change_percentage = (
            changed_pixels / total_pixels
        ) * 100

        # -----------------------------
        # RESULTS
        # -----------------------------
        st.success("Analysis completed successfully!")

        st.divider()

        st.subheader("🧠 Query Understanding")

        st.info(
            f"**Detected analysis:** Temporal Change Detection\n\n"
            f"**User query:** {query}"
        )

        # -----------------------------
        # IMAGE RESULTS
        # -----------------------------
        st.subheader("🗺️ Change Detection Result")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.image(
                before,
                caption="Before",
                use_container_width=True
            )

        with result_col2:
            st.image(
                after,
                caption="After",
                use_container_width=True
            )

        with result_col3:

            fig, ax = plt.subplots()

            ax.imshow(change_mask, cmap="Reds")
            ax.set_title("Detected Change")
            ax.axis("off")

            st.pyplot(fig)

            plt.close(fig)

        # -----------------------------
        # STATISTICS
        # -----------------------------
        st.divider()

        st.subheader("📊 Analysis Summary")

        stat1, stat2, stat3 = st.columns(3)

        with stat1:
            st.metric(
                "Changed Area",
                f"{change_percentage:.2f}%"
            )

        with stat2:
            st.metric(
                "Pixels Analysed",
                f"{total_pixels:,}"
            )

        with stat3:
            st.metric(
                "Change Threshold",
                threshold
            )

        # -----------------------------
        # EXPLANATION
        # -----------------------------
        st.subheader("🔎 Explanation")

        st.write(
            f"SATQUERY compared the Before and After images "
            f"pixel-by-pixel. Approximately **{change_percentage:.2f}%** "
            f"of the analyzed image shows significant visual change "
            f"according to the selected threshold."
        )

        st.caption(
            "Prototype uses RGB image change detection. "
            "Multispectral/NDVI analysis will be added in the next version."
        )