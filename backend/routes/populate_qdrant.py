from fastapi import APIRouter

router = APIRouter()


@router.post("/populate-qdrant")
async def populate_qdrant_endpoint():
    from scripts.populate_qdrant import main as populate_main

    populate_main()
    return {"status": "done"}
