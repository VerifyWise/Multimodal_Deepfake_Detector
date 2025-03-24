from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime


def generate_pdf_report(video_path, result, confidence, thumbnail_path=None):
    """
    Generates a detailed PDF report for video deepfake detection.
    """
    # ✅ Save directly to Downloads
    downloads_folder = os.path.expanduser("~") + "/Downloads"
    report_filename = f"video_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_path = os.path.join(downloads_folder, report_filename)

    c = canvas.Canvas(report_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 750, "Video Deepfake Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"File Name: {os.path.basename(video_path)}")
    c.drawString(50, 700, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 680, f"Result: {result}")
    c.drawString(50, 660, f"Confidence Score: {confidence:.2f}%")

    if thumbnail_path and os.path.exists(thumbnail_path):
        c.drawInlineImage(thumbnail_path, 50, 400, width=200, height=150)

    c.save()

    print(f"✅ PDF report saved at: {report_path}")  # Debugging line
    return report_path  # ✅ Correctly return the path