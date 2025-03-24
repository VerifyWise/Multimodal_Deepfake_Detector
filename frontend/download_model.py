import os
import requests
from tqdm import tqdm

# Folder to store models
MODEL_DIR = "models"

# URLs of the model files from GitHub Releases
MODEL_FILES = {
    "xception_deepfake_detector.h5": "https://github.com/javeriaahmed21/Multimodal-Deepfake-Detection/releases/download/v1.0/xception_deepfake_detector.h5",
    "xception_model.h5": "https://github.com/javeriaahmed21/Multimodal-Deepfake-Detection/releases/download/v1.0/xception_model.h5",
    "cnn-lstm-adversarial-trained.1.h5" : "https://github.com/javeriaahmed21/Multimodal-Deepfake-Detection/releases/download/v1.0/cnn-lstm-adversarial-trained.1.h5"
}
def download_file(url, save_path):
    """Download a file with a progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 KB

    with open(save_path, "wb") as file, tqdm(
        desc=save_path,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

def ensure_models_exist():
    """Check if model files exist, if not, download them."""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)  # Create the models directory if it doesn’t exist

    for file_name, url in MODEL_FILES.items():
        file_path = os.path.join(MODEL_DIR, file_name)
        if not os.path.exists(file_path):
            print(f"Downloading {file_name}...")
            download_file(url, file_path)
        else:
            print(f"{file_name} already exists. Skipping download.")

if __name__ == "__main__":
    ensure_models_exist()
