from fastapi import APIRouter, HTTPException

from backend.models.schemas import AccessibilityRequest
from backend.services.gemini_service import generate_accessibility


# ==================================================
# ROUTER
# ==================================================

router = APIRouter(
    prefix="/api/accessibility",
    tags=["Accessibility"]
)


# ==================================================
# GENERATE ACCESSIBILITY DESCRIPTION
# ==================================================

@router.post("/generate")
def generate_accessibility_description(
    request: AccessibilityRequest
):

    try:

        result = generate_accessibility(
            content=request.content,
            language=request.language
        )

        return {
            "success": True,
            "description": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )