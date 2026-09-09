# =========================================================
# SATQUERY-AI
# UI / SPACE BACKGROUND
# =========================================================

from pathlib import Path
import base64
import streamlit as st


def apply_space_background():

    # Project folder
    project_root = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    # Your exact image name
    image_path = (
        project_root
        / "assets"
        / "satquery_space1.png"
    )

    # Check image exists
    if not image_path.exists():

        st.warning(
            "Space background not found. "
            "Make sure satquery_space1.png "
            "is inside the assets folder."
        )

        return


    # Read image
    with open(
        image_path,
        "rb"
    ) as image_file:

        encoded_image = (
            base64.b64encode(
                image_file.read()
            ).decode()
        )


    # Apply background
    st.markdown(
        f"""
        <style>

        /* =====================================
           SPACE BACKGROUND
           ===================================== */

        .stApp {{

            background-image:

                linear-gradient(
                    rgba(0, 0, 0, 0.55),
                    rgba(0, 0, 0, 0.72)
                ),

                url(
                    "data:image/png;base64,
                    {encoded_image}"
                );

            background-size: cover;

            background-position: center;

            background-attachment: fixed;

        }}


        /* =====================================
           MAIN TITLE
           ===================================== */

        .main-title {{

            font-size: 46px;

            font-weight: 800;

            letter-spacing: 1px;

            text-shadow:
                0 0 18px
                rgba(0, 170, 255, 0.8);

        }}


        /* =====================================
           SUBTITLE
           ===================================== */

        .subtitle {{

            font-size: 18px;

            opacity: 0.9;

        }}


        /* =====================================
           FILE UPLOADER
           ===================================== */

        section[data-testid="stFileUploaderDropzone"] {{

            background:
                rgba(5, 15, 35, 0.70);

            border-radius:
                14px;

            border:
                1px solid
                rgba(100, 180, 255, 0.35);

        }}


        /* =====================================
           BUTTONS
           ===================================== */

        .stButton > button {{

            border-radius:
                10px;

            font-weight:
                600;

        }}


        </style>
        """,
        unsafe_allow_html=True
    )