# 🔍 Multimodal Deepfake Detector
![Project Banner](https://via.placeholder.com/1200x400.png?text=Multimodal+Deepfake+Detector)

> **A powerful AI-based tool to detect deepfakes in images, videos, and audio with high accuracy.**

---

## 🚀 Key Features
✅ Detect deepfakes across multiple media formats.  
✅ Generates detailed PDF reports for analysis.  
✅ User-friendly interface with animations and mascot assistance.  
✅ Secure login with data stored in an SQLite database.  

---

## 📚 How It Works
1. **Login/Register:** Secure user authentication to manage data.  
2. **Upload Media:** Supports audio, video, and image files.  
3. **Deepfake Detection:** Instant results with confidence score.  
4. **PDF Report:** Generates a detailed PDF with findings.  

---

## 🖥️ Installation Guide
```bash
# Clone the repository
git clone https://github.com/your-username/Multimodal_Deepfake_Detector.git

# Navigate to the project directory
cd Multimodal_Deepfake_Detector

# Install required packages
pip install -r requirements.txt

# Run the application
streamlit run app.py
📦 Multimodal_Deepfake_Detector
┣ 📂 models
┃ ┣ 📜 xception_model.h5       # Audio Model
┃ ┣ 📜 cnn-lstm-adversarial-trained.h5   # Video Model
┃ ┣ 📜 image_model.h5          # Image Model
┣ 📂 pages
┃ ┣ 📜 upload.py               # File upload and prediction
┃ ┣ 📜 report.py               # PDF report generation
┣ 📜 app.py                    # Main Streamlit app
┣ 📜 requirements.txt          # Project dependencies
┗ 📜 README.md                  # Project overview

## 📸 Screenshots
| Home Page                  | Upload Section              |
|----------------------------|----------------------------|
| ![Home](https://via.placeholder.com/400x300.png?text=Home+Page) | ![Upload](https://via.placeholder.com/400x300.png?text=Upload+Section) |

## 🤝 Contributing
We welcome contributions! Please check our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📞 Contact Us
📧 Email: [verifywise6924@gmail.com](mailto:verifywise6924@gmail.com)  
📞 Phone: +91-7385107129  

