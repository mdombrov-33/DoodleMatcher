from pathlib import Path
import numpy as np
from PIL import Image
import onnxruntime as ort

# Setup
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models/clip/clip-vit-base-patch32.onnx"

# Check model exists
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

# Load model
session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

# Get the actual input name from the model
input_name = session.get_inputs()[0].name
print(f"Model input name: {input_name}")


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Convert PIL image to model input format with proper CLIP preprocessing."""
    # Resize and convert to RGB
    image = image.convert("RGB").resize((224, 224))

    # Convert to array and normalize to [-1, 1] range (CLIP standard)
    img_array = np.array(image, dtype=np.float32)
    img_array = (img_array / 255.0 - 0.5) / 0.5  # Normalize to [-1, 1]

    # Change from HWC to CHW format
    img_array = img_array.transpose(2, 0, 1)

    # Add batch dimension: (1, 3, 224, 224)
    img_array = img_array[np.newaxis, ...]

    return img_array


def get_image_embedding(image: Image.Image) -> np.ndarray:
    """Get normalized embedding for an image."""
    try:
        # Preprocess
        input_data = preprocess_image(image)

        # Run inference with correct input name
        outputs = session.run(None, {input_name: input_data})
        embedding = outputs[0]  # First output should be image embeddings

        # Remove batch dimension if needed
        if embedding.ndim == 2 and embedding.shape[0] == 1:
            embedding = embedding[0]

        # Convert to float64 for better precision
        embedding = embedding.astype(np.float64)

        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding

    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
