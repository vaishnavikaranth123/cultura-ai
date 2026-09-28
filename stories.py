from fastapi import APIRouter, HTTPException

from backend.models.schemas import StoryRequest

from backend.services.gemini_service import (
    generate_creator_story,
)


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    prefix="/api/stories",
    tags=["Creator Stories"],
)


# ==========================================
# GENERATE CREATOR STORY
# ==========================================

@router.post("/generate")
def generate_story(
    request: StoryRequest
):

    try:

        story = generate_creator_story(

            creator_name=request.creator_name,

            work_title=request.work_title,

            creator_description=
                request.creator_description,

            cultural_context=
                request.cultural_context,

            audience=
                request.audience,

            language=
                request.language,

            style=
                request.style,

        )

        return {

            "success": True,

            "story": story,

        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error),

        )