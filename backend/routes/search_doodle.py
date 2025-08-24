import base64
import binascii
import io
import time
from fastapi import HTTPException, APIRouter
from PIL import Image

from models.search import SearchRequest, SearchResponse, MatchResult
from services.clip_service import get_image_embedding
from services.qdrant_service import search_similar_images

router = APIRouter()


@router.post("/search-doodle", response_model=SearchResponse)
async def search_doodle(request: SearchRequest):
    start_time = time.time()

    try:
        # 1. Decode base64 image
        # Handle both with and without data URL prefix
        image_data = request.image_data
        if image_data.startswith("data:image/png;base64,"):
            image_data = image_data.replace("data:image/png;base64,", "")

        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)

        # 2. Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # 3. Generate CLIP embedding
        embedding = get_image_embedding(image)
        if embedding is None:
            raise HTTPException(status_code=500, detail="Failed to generate embedding")

        # 4. Search Qdrant for similar images
        # This returns list of (photo_url, similarity_score, animal_type)
        search_results = search_similar_images(embedding, limit=3)

        # 5. Convert similarity scores to confidence percentages
        matches = []
        for photo_url, similarity, animal_type in search_results:
            # Convert cosine similarity (-1 to 1) to confidence (0-100%)
            confidence = max(0, min(100, (similarity + 1) * 50))
            matches.append(
                MatchResult(
                    photo_url=photo_url,
                    confidence=round(confidence, 1),
                    animal_type=animal_type,
                )
            )

        # 6. Calculate response time
        search_time_ms = int((time.time() - start_time) * 1000)

        return SearchResponse(matches=matches, search_time_ms=search_time_ms)

    except binascii.Error:  # Fixed: now properly imported
        raise HTTPException(status_code=400, detail="Invalid base64 image data")
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")
