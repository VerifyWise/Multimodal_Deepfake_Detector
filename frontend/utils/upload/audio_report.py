from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime


def generate_spectrogram(audio_path, output_path="spectrogram.png"):
    """Generates and saves a spectrogram from an audio file."""
    y, sr = librosa.load(audio_path, sr=16000)
    plt.figure(figsize=(8, 3))
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_DB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_DB, sr=sr, x_axis="time", y_axis="mel")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def generate_pdf_report(audio_path, label, confidence, output_pdf="audio_report.pdf"):
    """Generates a PDF report for audio deepfake detection."""
    filename = os.path.basename(audio_path)
    spectrogram_path = generate_spectrogram(audio_path)
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 50, "Audio Deepfake Detection Report")
    c.setFont("Helvetica", 10)
    c.drawString(200, height - 70, "---------------------------------------------")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "📌 Input Audio Details")
    c.setFont("Helvetica", 10)
    c.drawString(70, height - 120, f"File Name: {filename}")
    c.drawString(70, height - 140, f"Classification: {label}")
    c.drawString(70, height - 160, f"Confidence Score: {confidence:.2f}%")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 190, "🔍 Spectrogram Analysis")
    c.drawInlineImage(spectrogram_path, 70, height - 450, width=400, height=200)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 480, "✅ Final Decision")
    c.setFont("Helvetica", 10)
    c.drawString(70, height - 500, f"The analyzed audio is classified as *{label}*.")
    c.drawString(70, height - 520, f"The confidence score is *{confidence:.2f}%*.")

    c.setFont("Helvetica", 8)
    c.drawString(50, 30, f"Report generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()
    return output_pdf
