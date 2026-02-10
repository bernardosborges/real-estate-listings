from fastapi import APIRouter

from app.jobs.enqueue import enqueue_photo_processing

router = APIRouter(prefix=f"{settings.API_PREFIX}/photos", tags=["Properties"])

# -----------------------------------------------
# ENDPOINT - CREATE PROPERTY
# -----------------------------------------------

@router.post(
        "/{photo_public_id}/process"
)
def process_photo(photo_public_id: str):
    enqueue_photo_processing(photo_public_id)
    return {"status": "queued"}