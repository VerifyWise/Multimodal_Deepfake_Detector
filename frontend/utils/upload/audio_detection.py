import streamlit as st
import tensorflow as tf
import numpy as np
import librosa
import librosa.display
import cv2
import os
import tempfile
from utils.upload.audio_report import generate_pdf_report  # Import report generator

# Load the pre-trained deepfake detection model
MODEL_PATH = os.path.join(os.getcwd(), "models", "xception_model.h5")

try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    st.error(f"Error loading model: {e}")
    model = None


def preprocess_audio(file_path, segment_length=5, sr=22050):
    """Converts an audio file into overlapping Mel spectrograms."""
    try:
        audio, _ = librosa.load(file_path, sr=sr)
        segment_samples = segment_length * sr
        spectrograms = []

        for start in range(0, len(audio), segment_samples):
            end = start + segment_samples
            segment = audio[start:end]
            if len(segment) < segment_samples:
                segment = np.pad(segment, (0, segment_samples - len(segment)))

            mel_spec = librosa.feature.melspectrogram(y=segment, sr=sr, n_mels=128)
            mel_spec = librosa.power_to_db(mel_spec, ref=np.max)
            mel_spec = np.stack((mel_spec,) * 3, axis=-1)
            mel_spec = cv2.resize(mel_spec, (150, 150))
            mel_spec = mel_spec / 255.0
            spectrograms.append(mel_spec)

        return np.array(spectrograms)
    except Exception as e:
        st.error(f"Error preprocessing audio: {e}")
        return None


def predict_audio(file_path):
    """Predicts if an audio file is real or fake."""
    spectrograms = preprocess_audio(file_path)
    if spectrograms is None or model is None:
        return "Error", 0.0  # Return default values in case of failure

    predictions = model.predict(spectrograms)

    if len(predictions.shape) > 1 and predictions.shape[1] == 2:
        labels = np.argmax(predictions, axis=1)
        confidence_scores = np.max(predictions, axis=1)  # Get max probability
    else:
        labels = (predictions.flatten() > 0.5).astype(int)
        confidence_scores = predictions.flatten()

    # Final label decision
    final_label = "Real" if np.mean(labels) > 0.5 else "Fake"
    confidence_score = round(float(np.mean(confidence_scores)) * 100, 2)

    return final_label, confidence_score

def process_audio(file_path):
    """Wrapper function for processing audio and generating a report."""
    label, confidence = predict_audio(file_path)
    report_path = None  # Initialize report path

    if label != "Error":
        report_path = generate_pdf_report(file_path, label, confidence)  # Generate report

    return label, confidence, report_path  # Now returning 3 values


def audio_detection_page():
    """Streamlit page for audio deepfake detection."""
    st.title("Audio Deepfake Detection")
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if uploaded_file:
        # ✅ Save uploaded file as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(uploaded_file.read())
            file_path = temp_audio.name  # ✅ Get temp file path

        st.audio(file_path, format="audio/wav")

        if st.button("Analyze Audio"):
            label, confidence, report_path = process_audio(file_path)  # ✅ Use temp file path
            if label != "Error":
                st.success(f"Prediction: {label} with confidence score: {confidence:.2f}%")
            else:
                st.error("Error processing the audio file. Please try again.")

        if report_path and st.button("Download Report"):
            with open(report_path, "rb") as f:
                st.download_button("Download Audio Report", f, file_name="audio_report.pdf", mime="application/pdf")

        # ✅ Delete temp file after processing
        os.remove(file_path)