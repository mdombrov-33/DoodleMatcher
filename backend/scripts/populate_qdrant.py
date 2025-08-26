"""
Purpose:
    - Populate Qdrant collection with animal photos from Unsplash
    - Download images, generate CLIP embeddings, and store vectors in Qdrant
    - Use deterministic UUIDs for points to satisfy Qdrant requirements

Usage:
    poetry run python -m scripts.populate_qdrant
"""

from dotenv import load_dotenv
from services.clip_service import get_image_embedding
from services.qdrant_service import (
    client,
    COLLECTION_NAME,
    create_collection_if_not_exists,
)
from services.unsplash_service import get_unsplash_photos, download_image
from constants.animals_list import ANIMALS
from qdrant_client.models import PointStruct
from utils.exceptions import UnsplashServiceError, ClipServiceError, QdrantServiceError
from utils.logger import logger
import uuid
import time

load_dotenv()


def process_and_store_photo(photo_data: dict) -> bool:
    """
    Download photo, generate embedding, and insert into Qdrant.
    Returns True if stored successfully, False otherwise.
    """

    logger.info(f"Processing photo {photo_data['id']} from {photo_data['url']}")

    try:
        image = download_image(photo_data["url"])
        if image is None:
            return False
    except UnsplashServiceError as e:
        logger.error(f"Could not download {photo_data['url']}: {e}", exc_info=True)
        return False

    try:
        embedding = get_image_embedding(image)
        if embedding is None:
            return False
    except ClipServiceError as e:
        logger.error(
            f"Could not generate embedding for {photo_data['url']}: {e}", exc_info=True
        )
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
        logger.info(f"Stored photo {photo_data['id']} in Qdrant")
        return True
    except QdrantServiceError as e:
        logger.error(f"Failed to store in Qdrant: {e}", exc_info=True)
        return False


def main():
    """
    Main routine:
        1. Ensure Qdrant collection exists
        2. Iterate over animal types
        3. Fetch photos from Unsplash
        4. Process and store each photo
    """
    logger.info("Starting Qdrant population script...")

    try:
        create_collection_if_not_exists()
    except QdrantServiceError as e:
        logger.error(f"Failed to create collection in Qdrant: {e}", exc_info=True)
        return

    total_stored = 0

    for animal in ANIMALS:
        photos = get_unsplash_photos(animal)
        if not photos:
            logger.warning(f"No photos found for animal: {animal}")
            continue

        for photo in photos:
            if process_and_store_photo(photo):
                total_stored += 1
            time.sleep(1)  # avoid hitting Unsplash rate limits

    logger.info(f"Finished. Total photos stored: {total_stored}")


if __name__ == "__main__":
    main()
