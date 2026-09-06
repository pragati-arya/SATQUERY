# 🛰️ SATQUERY AI

### An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis

SATQUERY AI is an AI-powered platform designed to make satellite-image analysis easier through natural-language queries.

Instead of requiring users to have advanced GIS or remote-sensing knowledge, SATQUERY aims to allow users to ask questions in simple language and receive visual, numerical, and evidence-based insights from satellite imagery.

---

## 🚀 Current Prototype

The current prototype demonstrates:

- 🛰️ Satellite image upload
- 💬 Natural-language query input
- 🔄 Before/After image comparison
- 🗺️ Pixel-level change detection
- 📊 Change percentage calculation
- 🔎 Visual change map
- 🧠 Query understanding interface

> **Note:** The current prototype uses RGB imagery for basic change detection. Multispectral and NDVI-based analysis will be incorporated in later versions.

---

## 🎯 Vision

SATQUERY aims to develop a query-driven remote-sensing analysis system capable of understanding user intent and selecting appropriate analysis workflows for different satellite-image tasks.

### Planned capabilities

- Natural-language satellite image querying
- Single-image visual question answering
- Temporal change detection
- Multispectral analysis
- NDVI-based vegetation monitoring
- Optical + SAR analysis
- Interactive geospatial visualization
- Evidence-grounded AI responses
- What-if analysis

---

## 🛠️ Technology Stack

- Python
- Streamlit
- OpenCV
- NumPy
- Pillow
- Matplotlib

---

## 📂 Project Structure

```text
SATQUERY/
│
├── app.py
├── requirements.txt
├── README.md
└── data/