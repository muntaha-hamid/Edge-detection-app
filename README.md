

## 🚀 Features

- Upload your own image or use sample images  
- Choose from **Canny**, **Sobel**, or **Laplacian** algorithms  
- Adjust parameters like thresholds, kernel size, and sigma  
- Real-time visualization of results  
- Clean, interactive UI built with Streamlit and custom CSS  



---

## ⚙️ How to Run

1. Clone this repository using git commit
2. Install dependencies:
   bash
   pip install -r requirements.txt

3. Run the app:
   streamlit run app.py

4. Open your browser at `http://localhost:8501`.



└── filters/
    ├── canny_filter.py
    ├── sobel_filter.py
    └── laplacian_filter.py
└── outputs/
    ├── canny_output.py
    ├── sobel_output.py
    └── laplacian_output.py
├── sample_images/
│   ├── abyssinian_cat.jpg
│   ├── human.jpg
    ├── road.jpg
├── utils/
    └── image_utils.py
├── app.py
├── README.md



### Outputs

###  Canny Edge Detection

![Canny Output](outputs/canny_output.png)

###  Sobel Edge Detection

![Sobel Output](outputs/sobel_output.png)

###  Laplacian Edge Detection

![Laplacian Output](outputs/laplacian_output.png)
