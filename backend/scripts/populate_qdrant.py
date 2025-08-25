"""
Purpose:
    - Populate Qdrant collection with animal photos from Unsplash
    - Download images, generate CLIP embeddings, and store vectors in Qdrant
    - Use deterministic UUIDs for points to satisfy Qdrant requirements

Usage:
    poetry run python -m scripts.populate_qdrant
"""

from services.clip_service import get_image_embedding
from services.qdrant_service import (
    client,
    COLLECTION_NAME,
    create_collection_if_not_exists,
)
from services.unsplash_service import get_unsplash_photos, download_image
from constants.animals_list import ANIMALS
from qdrant_client.models import PointStruct
import uuid
import time


def process_and_store_photo(photo_data: dict) -> bool:
    """
    Download photo, generate embedding, and insert into Qdrant.
    Returns True if stored successfully, False otherwise.
    """
    print(f"Processing {photo_data['animal_type']} photo: {photo_data['id']}")

    image = download_image(photo_data["url"])
    if image is None:
        return False

    embedding = get_image_embedding(image)
    if embedding is None:
        return False

    point = PointStruct(
        id=str(uuid.uuid5(uuid.NAMESPACE_URL, photo_data["id"])),
        vector=embedding.tolist(),
        payload={
            "photo_url": photo_data["url"],
            "animal_type": photo_data["animal_type"],
            "photographer": photo_data["photographer"],
            "source": "unsplash",
        },
    )

    try:
        client.upsert(collection_name=COLLECTION_NAME, points=[point])
        print(f"[OK] Stored {photo_data['animal_type']} photo in Qdrant")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to store in Qdrant: {e}")
        return False


def main():
    """
    Main routine:
        1. Ensure Qdrant collection exists
        2. Iterate over animal types
        3. Fetch photos from Unsplash
        4. Process and store each photo
    """
    print("Starting database population")
    create_collection_if_not_exists()
    total_stored = 0

    for animal in ANIMALS:
        photos = get_unsplash_photos(animal)
        if not photos:
            print(f"[WARNING] No photos found for {animal}")
            continue

        for photo in photos:
            if process_and_store_photo(photo):
                total_stored += 1
            time.sleep(1)  # avoid hitting Unsplash rate limits

    print(f"\nDone! Stored {total_stored} photos in Qdrant")


if __name__ == "__main__":
    main()
