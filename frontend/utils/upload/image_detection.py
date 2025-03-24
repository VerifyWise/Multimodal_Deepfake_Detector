import streamlit as st
import tensorflow as tf
import numpy as np
import os
import tempfile
from tensorflow.keras.preprocessing import image
from utils.upload.image_report import generate_pdf_report  # Import fixed PDF report generator

# Load the pre-trained deepfake detection model
MODEL_PATH = os.path.join(os.getcwd(), "models", "xception_deepfake_detector.h5")

try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    st.error(f"Error loading model: {e}")
    model = None

# ✅ Image Preprocessing
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(299, 299))  # Resize for Xception model
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# ✅ Detect Deepfake in Image
def detect_deepfake(img_path):
    img_array = preprocess_image(img_path)
    if model is None:
        return "Error", 0.0

    prediction = model.predict(img_array)[0][0]  # Get prediction probability
    confidence = round(float(prediction) * 100, 2)

    # Determine label
    label = "Fake" if prediction > 0.5 else "Real"

    return label, confidence

# ✅ Process Image and Generate PDF Report
def process_image(file_path):
    label, confidence = detect_deepfake(file_path)
    if label == "Error":
        return label, confidence, None  # No report generated

    # ✅ Generate PDF Report (Saved in Downloads)
    report_path = generate_pdf_report(file_path, label, confidence)
    return label, confidence, report_path

# ✅ Streamlit UI for Image Detection
def image_detection_page():
    st.title("🖼️ Image Deepfake Detection")
    uploaded_file = st.file_uploader("📤 Upload an image file", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        # ✅ Save uploaded file as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            temp_image.write(uploaded_file.read())
            file_path = temp_image.name  # ✅ Get temp file path

        # ✅ Fixed deprecated warning
        st.image(file_path, caption="📸 Uploaded Image", use_container_width=True)

        if st.button("🔍 Analyze Image"):
            label, confidence, report_path = process_image(file_path)

            if label != "Error":
                st.success(f"✅ Prediction: **{label}** with confidence **{confidence:.2f}%**")

                # ✅ Display Report Save Confirmation
                if report_path:
                    st.success(f"📄 PDF Report saved at: **{report_path}**")
                    st.download_button("📥 Download Image Report", open(report_path, "rb"), file_name="image_report.pdf", mime="application/pdf")
            else:
                st.error("❌ Error processing the image file. Please try again.")

        # ✅ Delete temp file after processing
        os.remove(file_path)

if __name__ == "__main__":
    image_detection_page()
