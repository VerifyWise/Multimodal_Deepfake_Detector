from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf_report(image_path, result, confidence):
    """
    Generates a detailed PDF report for image deepfake detection.
    """
    # ✅ Save directly to Downloads
    downloads_folder = os.path.expanduser("~") + "/Downloads"
    report_filename = f"image_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    report_path = os.path.join(downloads_folder, report_filename)

    # ✅ Create PDF
    c = canvas.Canvas(report_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, 750, "Image Deepfake Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"File Name: {os.path.basename(image_path)}")
    c.drawString(50, 700, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 680, f"Result: {result}")
    c.drawString(50, 660, f"Confidence Score: {confidence:.2f}%")

    c.save()

    print(f"✅ PDF report saved at: {report_path}")  # Debugging line
    return report_path  # ✅ Correctly return the path
