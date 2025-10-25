import streamlit as st
import os
from utils.image_utils import read_image
from filters.canny_filter import apply_canny
from filters.sobel_filter import apply_sobel
from filters.laplacian_filter import apply_laplacian


st.set_page_config(
    page_title="Edge Detection Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #1f77b4;
        font-size: 3rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    .subtitle {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .stRadio > label {
        font-weight: 600;
        font-size: 1.1rem;
        color: #333;
    }
    .algorithm-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .info-box {
        background: #f0f7ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 2rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .image-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stSelectbox > label, .stSlider > label {
        font-weight: 600;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Edge Detection Visualizer")
st.markdown('<p class="subtitle">Upload an image or choose a sample, then explore different edge detection algorithms with real-time parameter adjustments!</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## Configuration")

# Image Selection
st.sidebar.markdown("### Image Source")
image_source = st.sidebar.radio(
    "Select where to get your image:",
    ["Upload Image", "Sample Gallery"],
    label_visibility="collapsed"
)

uploaded_file = None
selected_sample = None

# Upload image or select from samples
if image_source == "Upload Image":
    uploaded_file = st.sidebar.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png", "bmp"],
        help="Supported formats: JPG, PNG, BMP"
    )
    if uploaded_file:
        st.sidebar.success("Image uploaded successfully!")
else:
    sample_dir = "sample_images"
    if os.path.exists(sample_dir):
        sample_images = [img for img in os.listdir(sample_dir) if img.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]
        
        if sample_images:
            selected_sample = st.sidebar.selectbox(
                "Pick a sample image:",
                sample_images,
                index=0
            )
        else:
            st.sidebar.warning("No sample images found in the sample_images folder.")
    else:
        st.sidebar.warning("Sample images directory not found.")

st.sidebar.markdown("---")

# Algorithm Selection
st.sidebar.markdown("### Algorithm")
algorithm = st.sidebar.radio(
    "Choose edge detection method:",
    ["Canny", "Sobel", "Laplacian"],
    index=0,
    label_visibility="collapsed"
)

# Algorithm info display
algorithm_info = {
    "Canny": "Multi-stage algorithm that detects a wide range of edges with high accuracy.",
    "Sobel": "Uses gradient-based approach to find edges in specific directions.",
    "Laplacian": "Second derivative method that detects edges using intensity changes."
}

st.sidebar.info(f"**{algorithm}**: {algorithm_info[algorithm]}")

st.sidebar.markdown("---")

# Parameters Section
st.sidebar.markdown("###  Parameters")

if algorithm == "Canny":
    threshold1 = st.sidebar.slider("Lower Threshold", 1, 255, 50, 1, help="Minimum intensity gradient required")
    threshold2 = st.sidebar.slider("Upper Threshold", 1, 255, 150, 1, help="Maximum intensity gradient threshold")
    ksize = st.sidebar.select_slider("Kernel Size", [3, 5, 7], value=3, help="Size of the Gaussian blur kernel")
    sigma = st.sidebar.slider("Sigma (Blur)", 0.5, 5.0, 1.0, 0.1, help="Gaussian blur standard deviation")

elif algorithm == "Sobel":
    ksize = st.sidebar.select_slider("Kernel Size", [1, 3, 5, 7], value=3, help="Size of the Sobel kernel")
    direction = st.sidebar.radio(
        "Edge Direction",
        ["X", "Y", "Both"],
        help="Direction of edge detection"
    )

elif algorithm == "Laplacian":
    ksize = st.sidebar.select_slider("Kernel Size", [1, 3, 5, 7], value=3, help="Size of the Laplacian kernel")

st.sidebar.markdown("---")
st.sidebar.markdown("**Tip**: Adjust parameters to see real-time changes in edge detection!")

# Main Content Area
if uploaded_file is not None or selected_sample is not None:
    try:
        # Load image
        if uploaded_file is not None:
            image, gray = read_image(uploaded_file)
        else:
            image_path = os.path.join("sample_images", selected_sample)
            image, gray = read_image(image_path)

        # Apply selected algorithm
        with st.spinner(f'Applying {algorithm} edge detection...'):
            if algorithm == "Canny":
                edges = apply_canny(gray, threshold1, threshold2, ksize, sigma)
            elif algorithm == "Sobel":
                edges = apply_sobel(gray, direction, ksize)
            elif algorithm == "Laplacian":
                edges = apply_laplacian(gray, ksize)

        # Display results
        st.markdown("## Results")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown("### Original Image")
            st.image(image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.markdown(f"### {algorithm} Detection")
            st.image(edges, use_container_width=True, clamp=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Additional info
        st.markdown("---")
        with st.expander("ℹAbout the Algorithm"):
            if algorithm == "Canny":
                st.markdown("""
                **Canny Edge Detection** is a multi-stage algorithm:
                1. **Noise Reduction**: Gaussian blur smooths the image
                2. **Gradient Calculation**: Finds intensity gradients
                3. **Non-maximum Suppression**: Thins edges
                4. **Double Threshold**: Classifies edges as strong or weak
                5. **Edge Tracking**: Connects edge pixels
                """)
            elif algorithm == "Sobel":
                st.markdown("""
                **Sobel Edge Detection** uses convolution with Sobel kernels:
                - Detects edges by calculating the gradient of image intensity
                - Can detect horizontal (X), vertical (Y), or both directions
                - Fast and efficient for real-time applications
                """)
            elif algorithm == "Laplacian":
                st.markdown("""
                **Laplacian Edge Detection** uses the second derivative:
                - Detects edges where intensity changes rapidly
                - Sensitive to noise (consider using blur preprocessing)
                - Detects edges in all directions simultaneously
                """)

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please make sure your image file is valid and try again.")

else:
    # Welcome screen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        ### Welcome to Edge Detection Visualizer!
        
        **Get started in 3 easy steps:**
        
        1.  **Upload an image** or select a sample from the sidebar
        2.  **Choose an algorithm** (Canny, Sobel, or Laplacian)
        3.  **Adjust parameters** and see results in real-time
        
        Edge detection is a fundamental technique in computer vision used to identify 
        boundaries of objects within images. Experiment with different algorithms and 
        parameters to see how they affect the results!
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample images preview if available
        if os.path.exists("sample_images"):
            st.markdown("###  Quick Start with Samples")
            st.info(" Select 'Sample Gallery' from the sidebar to try out sample images!")