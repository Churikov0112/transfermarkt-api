from fastapi import APIRouter

from app.services.coaches.profile import TransfermarktCoachProfile

router = APIRouter()


@router.get("/{coach_id}/profile")
def get_coach_profile(coach_id: str):
    """
    Get coach profile by coach ID.

    Example: /coaches/2711/profile
    """
    tfmkt = TransfermarktCoachProfile(coach_id=coach_id)
    result = tfmkt.get_coach_profile()
    return result