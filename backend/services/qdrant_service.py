"""
Purpose:
    - Provide Qdrant client and utility functions for storing and searching image embeddings
    - Handle collection creation and similarity search
    - Centralized service for other scripts to interact with Qdrant

Usage:
    from services.qdrant_service import (
        client,
        COLLECTION_NAME,
        create_collection_if_not_exists,
        search_similar_images
    )
"""

from qdrant_client import QdrantClient

import os
from qdrant_client.models import Distance, VectorParams
import numpy as np
from typing import List, Tuple
from utils.exceptions import QdrantServiceError


#! Qdrant Client Configuration
# This section sets up the connection Qdrant vector database.
# The same code works for both local development and production.
# We control which instance is used via the QDRANT_URL environment variable.

# Local development (optional)
# Uncomment these lines if we want to populate a local Qdrant instance:
# from dotenv import load_dotenv
# load_dotenv()  # Load environment variables from .env
# QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
# USE_HTTPS = False
# PORT = 6333

# Production (default)
# For deployed backend, set QDRANT_URL in .env file to Railway Qdrant URL
QDRANT_URL = os.getenv("QDRANT_URL")  # Must be set in .env for production
USE_HTTPS = True  # Railway Qdrant uses HTTPS
PORT = 443  # Default HTTPS port

# Initialize the Qdrant client
client = QdrantClient(
    url=QDRANT_URL,
    timeout=60,  # * Wait up to 60 seconds for requests, important for Railway to avoid Qdrant creating timeouts
    https=USE_HTTPS,
    port=PORT,
)

# Collection name for storing animal photo embeddings
COLLECTION_NAME = "animal_photos"


def search_similar_images(
    embedding: np.ndarray, limit: int = 3
) -> List[Tuple[str, float, str, str]]:
    """
    Search for images similar to the given embedding in Qdrant.

    Args:
        embedding: CLIP embedding vector
        limit: Number of results to return

    Returns:
        List of (photo_url, similarity_score, animal_type) tuples
    """
    try:
        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embedding.tolist(),
            limit=limit,
            with_payload=True,
        )

        results = []
        for result in search_results:
            if result.payload is not None:
                photo_url = result.payload.get("photo_url", "")
                animal_type = result.payload.get("animal_type", "unknown")
                photographer = result.payload.get("photographer", "unknown")
                similarity_score = result.score
                results.append((photo_url, similarity_score, animal_type, photographer))

        return results

    except Exception as e:
        raise QdrantServiceError(f"Error searching similar images: {e}")


def create_collection_if_not_exists():
    """
    Create the animal_photos collection if it doesn't exist.

    Uses 512-D vectors and cosine distance for embeddings.
    """
    try:
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]

        if COLLECTION_NAME not in collection_names:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=512,
                    distance=Distance.COSINE,
                ),
            )
            print(f"Created collection: {COLLECTION_NAME}")
        else:
            print(f"Collection {COLLECTION_NAME} already exists")

    except Exception as e:
        raise QdrantServiceError(f"Error creating collection: {e}")
