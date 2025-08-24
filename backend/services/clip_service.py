import requests
import numpy as np
from PIL import Image
import io
from typing import Optional
import os

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch16"


def get_image_embedding(image: Image.Image) -> Optional[np.ndarray]:
    """
    Takes a PIL Image and returns its CLIP embedding using Hugging Face API.
    """
    try:
        # Convert PIL Image to bytes
        img_buffer = io.BytesIO()
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Prepare the API request
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

        # Send image to Hugging Face API
        response = requests.post(
            HF_API_URL,
            headers=headers,
            files={"inputs": img_buffer.getvalue()},
            timeout=30,
        )

        if response.status_code == 200:
            # The API returns the embedding directly
            embedding = np.array(response.json())

            # Normalize the embedding
            embedding = embedding / np.linalg.norm(embedding)

            return embedding.flatten()
        else:
            print(f"HF API error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None
