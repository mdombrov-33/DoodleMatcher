"""
Purpose:
    - Provide functions to generate CLIP image embeddings from PIL Images
    - Handle preprocessing, ONNX inference, and L2 normalization
    - Centralized service for embedding generation used across scripts

Usage:
    from services.clip_service import get_image_embedding
    embedding = get_image_embedding(pil_image)
"""

from pathlib import Path
import numpy as np
from PIL import Image
import onnxruntime as ort
from utils.exceptions import ClipServiceError

# Setup ONNX model path
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models/clip/clip-vit-base-patch32.onnx"

# Ensure model exists
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

# Load ONNX session (CPU)
session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

# Retrieve input name dynamically
input_name = session.get_inputs()[0].name
print(f"Model input name: {input_name}")


def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Convert a PIL image to the input format expected by the CLIP ONNX model.

    Steps:
        1. Convert to RGB and resize to 224x224
        2. Normalize pixel values to [-1, 1] range (CLIP standard)
        3. Convert from HWC to CHW
        4. Add batch dimension
    Returns:
        np.ndarray of shape (1, 3, 224, 224)
    """
    image = image.convert("RGB").resize((224, 224))
    img_array = np.array(image, dtype=np.float32)
    img_array = (img_array / 255.0 - 0.5) / 0.5
    img_array = img_array.transpose(2, 0, 1)
    img_array = img_array[np.newaxis, ...]
    return img_array


def get_image_embedding(image: Image.Image) -> np.ndarray:
    """
    Generate a normalized embedding vector for a given image.

    Steps:
        1. Preprocess the image
        2. Run ONNX inference
        3. Remove batch dimension
        4. Convert to float64
        5. Normalize embedding to unit length (L2 norm = 1)

    Returns:
        np.ndarray of shape (512,) or None on failure
    """
    try:
        input_data = preprocess_image(image)
        outputs = session.run(None, {input_name: input_data})
        embedding = outputs[0]

        if embedding.ndim == 2 and embedding.shape[0] == 1:
            embedding = embedding[0]

        embedding = embedding.astype(np.float64)
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding

    except Exception as e:
        raise ClipServiceError(f"Error generating embedding: {e}")
