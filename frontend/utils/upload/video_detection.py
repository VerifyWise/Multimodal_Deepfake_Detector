import os
import cv2
import numpy as np
import tempfile
import joblib
import streamlit as st
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import Xception
from tensorflow.keras.preprocessing.sequence import pad_sequences

from moviepy import VideoFileClip
from mtcnn import MTCNN
import librosa
from sklearn.preprocessing import StandardScaler
from scipy.special import softmax
from utils.upload.video_report import generate_pdf_report  # ✅ Correct import

# ===========================
# 🎯 Load Pre-trained Models
# ===========================
MODEL_PATH = r"C:\Users\JAVERIA AHMED\PycharmProjects\MDD Website\models\cnn-lstm-adversarial-trained.h5"
model = load_model(MODEL_PATH)
xception_model = Xception(weights='imagenet', include_top=False, pooling='avg')


# ===========================
# 🛠 Helper Functions
# ===========================

def extract_frames(video_path, resize_dim=(299, 299), num_frames=30):
    """
    Extracts evenly spaced frames from a video.
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)

    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, resize_dim)
            frames.append(frame)
    cap.release()
    return np.array(frames)


def extract_thumbnail(video_path, output_path="thumbnail.jpg"):
    """
    Extracts a thumbnail from the middle frame of the video.
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = total_frames // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
    cap.release()
    return output_path if os.path.exists(output_path) else None


def detect_faces(frames):
    """
    Detects faces in the extracted frames.
    """
    detector = MTCNN()
    faces = []
    for frame in frames:
        detections = detector.detect_faces(frame)
        for detection in detections:
            if detection['confidence'] > 0.9:
                x, y, width, height = detection['box']
                x, y = max(0, x), max(0, y)
                face = frame[y:y + height, x:x + width]
                resized_face = cv2.resize(face, (299, 299)) / 255.0
                faces.append(resized_face)
    return np.array(faces) if faces else np.zeros((1, 299, 299, 3))


def extract_xception_features(faces):
    return np.array([xception_model.predict(np.expand_dims(face, axis=0))[0] for face in faces])


def process_audio(video_path):
    """
    Extracts audio from the video and converts it into a Mel spectrogram.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        video_clip = VideoFileClip(video_path)
        video_clip.audio.write_audiofile(temp_audio.name)
        video_clip.close()

        audio, sr = librosa.load(temp_audio.name, sr=None)
        mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
        return librosa.power_to_db(mel_spectrogram, ref=np.max)


def combine_features(xception_features, mel_spectrogram):
    mel_flat = mel_spectrogram.flatten()
    expected_dim = 4454 - xception_features.shape[1]
    mel_resized = np.resize(mel_flat, (xception_features.shape[0], expected_dim))
    return np.concatenate((xception_features, mel_resized), axis=1)


def predict_video(video_path):
    """
    Predicts if a video is Real or Deepfake.
    """
    frames = extract_frames(video_path)
    faces = detect_faces(frames)
    xception_features = extract_xception_features(faces)
    mel_spectrogram = process_audio(video_path)
    combined_features = combine_features(xception_features, mel_spectrogram)

    scaler = StandardScaler()
    combined_features = scaler.fit_transform(combined_features)

    sequences = pad_sequences([combined_features], padding='post', dtype='float32', maxlen=30)
    predictions = model.predict(np.array(sequences))
    predictions = np.mean(softmax(predictions, axis=1), axis=0)

    confidence = round(max(0, min(1, predictions[1])) * 100, 2)  # ✅ Rounded to 2 decimal places
    result = "DEEPFAKE" if confidence > 50 else "REAL"

    return result, confidence


def process_video(video_path):
    """
    Processes the video and generates a report.
    """
    result, confidence = predict_video(video_path)
    thumbnail_path = extract_thumbnail(video_path)
    report_path = generate_pdf_report(video_path, result, confidence, thumbnail_path)
    return result, confidence, report_path


# ===========================
# 🎬 Streamlit Interface
# ===========================
def video_detection_page():
    st.title("Video Deepfake Detection")
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.read())
            file_path = temp_video.name

        if st.button("Analyze Video"):
            result, confidence, report_path = process_video(file_path)
            st.success(f"Prediction: {result} with confidence score: {confidence:.2f}%")  # ✅ Confidence formatted correctly

            # ✅ Ensure the file is read in binary mode for downloading
            if os.path.exists(report_path):
                with open(report_path, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                    st.download_button(label="Download Video Report",
                                       data=pdf_bytes,
                                       file_name="video_report.pdf",
                                       mime="application/pdf")

        os.remove(file_path)
