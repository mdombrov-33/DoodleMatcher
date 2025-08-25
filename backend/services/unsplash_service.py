import os
import requests
from PIL import Image
import io

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")


def get_unsplash_photos(animal: str, count: int = 15) -> list[dict]:
    """Query Unsplash API for images of the given animal."""
    if not UNSPLASH_API_KEY:
        print("[WARNING] UNSPLASH_API_KEY not set")
        return []

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": f"{animal} animal",
        "per_page": count,
        "client_id": UNSPLASH_API_KEY,
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
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
    except Exception as e:
        print(f"[ERROR] Unsplash API fetch failed: {e}")
        return []


def download_image(url: str) -> Image.Image | None:
    """Download an image from a URL and return a PIL Image or None."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return Image.open(io.BytesIO(resp.content)).convert("RGB")
    except Exception as e:
        print(f"[ERROR] Failed to download image {url}: {e}")
        return None
