from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import numpy as np
from typing import List, Tuple

# Initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")  # Change for production
COLLECTION_NAME = "animal_photos"


def search_similar_images(
    embedding: np.ndarray, limit: int = 3
) -> List[Tuple[str, float, str]]:
    """
    Search for similar images in Qdrant

    Args:
        embedding: CLIP embedding vector
        limit: Number of results to return

    Returns:
        List of (photo_url, similarity_score, animal_type) tuples
    """
    try:
        # Search in Qdrant
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
                similarity_score = result.score

            results.append((photo_url, similarity_score, animal_type))

        return results

    except Exception as e:
        print(f"Qdrant search error: {e}")
        return []


def create_collection_if_not_exists():
    """Create the animal photos collection if it doesn't exist"""
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
        print(f"Error creating collection: {e}")
