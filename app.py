import streamlit as st
import os
from utils.image_utils import read_image
from filters.canny_filter import apply_canny
from filters.sobel_filter import apply_sobel
from filters.laplacian_filter import apply_laplacian


st.set_page_config(page_title="Edge Detection Visualizer", layout="wide")

st.title("Edge Detection Visualizer")
st.markdown("Upload an image **or choose a sample** and explore how different edge detection algorithms work interactively!")

# side bar
st.sidebar.header("⚙️ Controls")

# upload image
image_source = st.sidebar.radio(
    "Select Image Source:",
    ["Upload your own", "Use a sample image"]
)

uploaded_file = None
selected_sample = None

# If user selects upload
if image_source == "Upload your own":
    uploaded_file = st.sidebar.file_uploader(
        "📤 Upload an Image",
        type=["jpg", "jpeg", "png", "bmp"],
        help="Upload a standard image file to begin processing."
    )

# If user selects sample image
else:
    sample_dir = "sample_images"
    sample_images = [img for img in os.listdir(sample_dir) if img.lower().endswith((".jpg", ".jpeg", ".png"))]

    selected_sample = st.sidebar.selectbox(
        "Choose a sample image",
        sample_images,
        index=0
    )

# algorithms
algorithm = st.sidebar.radio(
    "Choose Algorithm",
    ["Canny", "Sobel", "Laplacian"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Adjust Parameters")

# parameters adjustment
if algorithm == "Canny":
    threshold1 = st.sidebar.slider("Lower Threshold", 1, 255, 50, 1)
    threshold2 = st.sidebar.slider("Upper Threshold", 1, 255, 150, 1)
    ksize = st.sidebar.select_slider("Kernel Size", [3, 5, 7], value=3)
    sigma = st.sidebar.slider("Sigma (Blur Intensity)", 0.5, 5.0, 1.0, 0.1)

elif algorithm == "Sobel":
    ksize = st.sidebar.select_slider("Kernel Size", [1, 3, 5, 7], value=3)
    direction = st.sidebar.radio("Direction", ["X", "Y", "Both"], horizontal=False)

elif algorithm == "Laplacian":
    ksize = st.sidebar.select_slider("Kernel Size", [1, 3, 5, 7], value=3)

st.sidebar.markdown("---")

# -error handling
if uploaded_file is not None or selected_sample is not None:
    # Load image either from upload or sample folder
    if uploaded_file is not None:
        image, gray = read_image(uploaded_file)
    else:
        image_path = os.path.join("sample_images", selected_sample)
        image, gray = read_image(image_path)

 
    if algorithm == "Canny":
        edges = apply_canny(gray, threshold1, threshold2, ksize, sigma)
    elif algorithm == "Sobel":
        edges = apply_sobel(gray, direction, ksize)
    elif algorithm == "Laplacian":
        edges = apply_laplacian(gray, ksize)

    # results
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)
    with col2:
        st.subheader(f"{algorithm} Edge Detection Result")
        st.image(edges, use_container_width=True, clamp=True)
else:
    st.info("Upload an image or select a sample from the sidebar to begin.")
