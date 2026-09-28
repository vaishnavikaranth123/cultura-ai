from fastapi import APIRouter, HTTPException

from backend.models.schemas import TranslationRequest
from backend.services.gemini_service import translate_content


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    prefix="/api/translation",
    tags=["Translation"]
)


# ==========================================
# TRANSLATE CREATOR CONTENT
# ==========================================

@router.post("/generate")
def translate_creator_content(
    request: TranslationRequest
):

    try:

        result = translate_content(
            content=request.content,
            target_language=request.target_language
        )

        return {
            "success": True,
            "translation": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )