"""
Purpose:
    - Test that the CLIP image encoder produces valid embeddings
    - Confirm embedding shape is 512-D
    - Confirm L2 normalization (embedding norm ~1.0)

Usage:
    poetry run python -m scripts.test_embedding
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np
from services.clip_service import get_image_embedding
from utils.logger import logger

#! Add backend/ to sys.path for imports
# Ensures we can import services.clip_service even if running from scripts/
BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(BACKEND_DIR))


#! Test image setup
# Place a small PNG image named 'test_cat.png' next to this script
TEST_IMAGE_PATH = Path(__file__).resolve().parent / "test_cat.png"
if not TEST_IMAGE_PATH.exists():
    raise FileNotFoundError(
        logger.error(
            f"Test image not found: {TEST_IMAGE_PATH}. Please place a PNG image here."
        )
    )

#! Load the image
image = Image.open(TEST_IMAGE_PATH)

#! Generate embedding
embedding = get_image_embedding(image)

if embedding is None:
    logger.error("Embedding generation failed")
else:
    #! Log embedding details
    logger.info(f"Embedding shape: {embedding.shape}")
    logger.info(f"Embedding dtype: {embedding.dtype}")
    norm = np.linalg.norm(embedding)
    logger.info(f"Embedding L2 norm: {norm:.4f}")

    #! Sanity check: shape and normalization
    if embedding.shape == (512,) and np.isclose(norm, 1.0, atol=1e-3):
        logger.info("Embedding generated correctly and normalized")
    else:
        logger.warning("Embedding shape or norm unexpected")
