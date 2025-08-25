import os
import time
import io
import requests
from PIL import Image

from services.clip_service import get_image_embedding
from services.qdrant_service import (
    client,
    COLLECTION_NAME,
    create_collection_if_not_exists,
)
from constants.animals_list import ANIMALS
import uuid
from qdrant_client.models import PointStruct

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")


def download_image(url: str) -> Image.Image | None:
    """Download an image from a URL and return a PIL Image or None."""
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return Image.open(io.BytesIO(resp.content))
        print(f"Failed to download {url}, status: {resp.status_code}")
    except Exception as e:
        print(f"Exception downloading {url}: {e}")
    return None


def get_unsplash_photos(animal: str, count: int = 15) -> list[dict]:
    """Query Unsplash API for images of the given animal."""
    if not UNSPLASH_API_KEY:
        print("UNSPLASH_API_KEY not set")
        return []

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": f"{animal} animal",
        "per_page": count,
        "client_id": UNSPLASH_API_KEY,
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return [
                {
                    "id": photo["id"],
                    "url": photo["urls"]["small"],
                    "animal_type": animal,
                    "photographer": photo["user"]["name"],
                }
                for photo in data.get("results", [])
            ]
        print(f"Unsplash API error {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"Exception fetching Unsplash photos: {e}")

    return []


def process_and_store_photo(photo_data: dict) -> bool:
    """
    Download photo, generate embedding, and insert into Qdrant.
    IDs are converted to UUID to satisfy Qdrant requirements.
    """
    print(
        f"Processing {photo_data['animal_type']} photo: {photo_data['id']} url: {photo_data['url']}"
    )

    # --- Download image ---
    try:
        image = Image.open(
            io.BytesIO(requests.get(photo_data["url"], timeout=10).content)
        )
        image = image.convert("RGB")
    except Exception as e:
        print(f"Failed to download image: {e}")
        return False

    # --- Generate embedding ---
    embedding = get_image_embedding(image)
    if embedding is None:
        print("Failed to generate embedding")
        return False

    # --- Create Qdrant point ---
    try:
        point = PointStruct(
            id=str(
                uuid.uuid5(uuid.NAMESPACE_URL, photo_data["id"])
            ),  # deterministic UUID
            vector=embedding.tolist(),
            payload={
                "photo_url": photo_data["url"],
                "animal_type": photo_data["animal_type"],
                "photographer": photo_data["photographer"],
                "source": "unsplash",
            },
        )
        client.upsert(collection_name=COLLECTION_NAME, points=[point])
        print(f"Stored {photo_data['animal_type']} photo in Qdrant")
        return True

    except Exception as e:
        print(f"Failed to store in Qdrant: {e}")
        return False


def main():
    print("Starting database population")
    create_collection_if_not_exists()
    total_stored = 0

    for animal in ANIMALS:
        print(f"\nGetting {animal} photos from Unsplash...")
        photos = get_unsplash_photos(animal)
        if not photos:
            print(f"No photos found for {animal}")
            continue

        for photo in photos:
            if process_and_store_photo(photo):
                total_stored += 1
            time.sleep(1)  # avoid hitting rate limits

    print(f"\nDone! Stored {total_stored} photos in Qdrant")
    try:
        col_info = client.get_collection(COLLECTION_NAME)
        print(f"Total vectors in collection: {col_info.points_count}")
    except Exception as e:
        print(f"Error fetching collection info: {e}")


if __name__ == "__main__":
    main()
