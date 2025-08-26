"""
Purpose:
    - Provide utility functions to fetch animal images from Unsplash
    - Download images and return as PIL.Image objects
    - Centralized service for other scripts to use Unsplash without duplicating code

Usage:
    from services.unsplash_service import get_unsplash_photos, download_image
"""

import os
import requests
from PIL import Image
import io

UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")


def get_unsplash_photos(animal: str, count: int = 100) -> list[dict]:
    """
    Query Unsplash API for images of a given animal.

    Args:
        animal: Name of the animal to search for
        count: Number of images to retrieve

    Returns:
        List of dictionaries containing photo metadata:
        {
            "id": str,
            "url": str,
            "animal_type": str,
            "photographer": str
        }
    """
    if not UNSPLASH_API_KEY:
        print("[WARNING] UNSPLASH_API_KEY not set")
        return []

    url = "https://api.unsplash.com/search/photos"
    photos = []
    page = 1
    per_page = 30  # Unsplash API max per_page
    try:
        while len(photos) < count:
            params = {
                "query": f"{animal} animal",
                "per_page": min(per_page, count - len(photos)),
                "page": page,
                "client_id": UNSPLASH_API_KEY,
            }
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                break
            photos.extend(
                [
                    {
                        "id": photo["id"],
                        "url": photo["urls"]["small"],
                        "animal_type": animal,
                        "photographer": photo["user"]["name"],
                    }
                    for photo in results
                ]
            )
            page += 1
        return photos[:count]
    except Exception as e:
        print(f"[ERROR] Unsplash API fetch failed: {e}")
        return []


def download_image(url: str) -> Image.Image | None:
    """
    Download an image from a URL and return a PIL Image.

    Args:
        url: Direct URL to the image

    Returns:
        PIL.Image.Image object or None if download failed
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return Image.open(io.BytesIO(resp.content))
    except Exception as e:
        print(f"[ERROR] Failed to download image {url}: {e}")
        return None
