from fastapi import HTTPException, APIRouter
import base64
import binascii
import io
import time
from PIL import Image

from schemas.search import SearchRequest, SearchResponse, MatchResult
from services.clip_service import get_image_embedding
from services.qdrant_service import search_similar_images
from utils.exceptions import SearchRequestError, QdrantServiceError, ClipServiceError
from utils.logger import logger

router = APIRouter()


@router.post("/search-doodle", response_model=SearchResponse)
async def search_doodle(request: SearchRequest):
    start_time = time.time()
    try:
        # 1. Decode base64 image
        image_data = request.image_data
        if image_data.startswith("data:image/png;base64,"):
            image_data = image_data.replace("data:image/png;base64,", "")

        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        except binascii.Error as e:
            raise SearchRequestError("Invalid base64 image data") from e
        except Exception as e:
            raise SearchRequestError("Failed to open image") from e

        # 2. Generate embedding
        try:
            embedding = get_image_embedding(image)
            if embedding is None:
                raise ClipServiceError("Embedding returned None")
        except ClipServiceError as e:
            logger.error(f"Embedding error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to generate embedding")

        # 3. Search Qdrant
        try:
            search_results = search_similar_images(embedding, limit=3)
        except QdrantServiceError as e:
            logger.error(f"Qdrant search error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Search failed")

        # 4. Convert to response
        matches = []
        for photo_url, similarity, animal_type, photographer in search_results:
            confidence = max(0, min(100, (similarity + 1) * 50))
            matches.append(
                MatchResult(
                    photo_url=photo_url,
                    confidence=round(confidence, 1),
                    animal_type=animal_type,
                    photographer=photographer,
                )
            )

        search_time_ms = int((time.time() - start_time) * 1000)
        return SearchResponse(matches=matches, search_time_ms=search_time_ms)

    except SearchRequestError as e:
        logger.warning(f"Bad search request: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected search error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Search failed")
