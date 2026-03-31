from fastapi import APIRouter

from app.services.coaches.profile import TransfermarktCoachProfile

router = APIRouter()


@router.get("/{coach_id}/image")
def get_coach_image(coach_id: str):
    """
    Get coach profile image by coach ID.

    Example: /coaches/2711/image
    """
    tfmkt = TransfermarktCoachProfile(coach_id=coach_id)
    result = tfmkt.get_coach_image()
    return result