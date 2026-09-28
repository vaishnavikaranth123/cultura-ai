from fastapi import APIRouter, HTTPException

from backend.models.schemas import ImmersiveRequest

from backend.services.gemini_service import (
    generate_immersive_experience
)


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    prefix="/api/immersive",
    tags=["AR / VR / Games"]
)


# ==========================================
# GENERATE IMMERSIVE EXPERIENCE
# ==========================================

@router.post("/generate")
def create_immersive_experience(
    request: ImmersiveRequest
):

    try:

        result = generate_immersive_experience(

            creator_name=request.creator_name,

            work_title=request.work_title,

            creator_description=
                request.creator_description,

            cultural_context=
                request.cultural_context,

            experience_type=
                request.experience_type,

            audience=
                request.audience

        )

        return {
            "success": True,
            "experience": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )