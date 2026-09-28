from fastapi import APIRouter, HTTPException

from backend.models.schemas import CreatorCreate

from backend.database.database import (
    create_creator,
    get_creators,
    get_creator
)


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    prefix="/api/creators",
    tags=["Creators"]
)


# ==========================================
# CREATE CREATOR
# ==========================================

@router.post("/")
def register_creator(
    data: CreatorCreate
):

    if not data.name.strip():

        raise HTTPException(
            status_code=400,
            detail="Creator name is required."
        )

    creator_id = create_creator(
        data
    )

    return {
        "success": True,
        "creator_id": creator_id,
        "message": "Creator profile created successfully."
    }


# ==========================================
# GET ALL CREATORS
# ==========================================

@router.get("/")
def list_creators():

    creators = get_creators()

    return {
        "success": True,
        "creators": creators
    }


# ==========================================
# GET ONE CREATOR
# ==========================================

@router.get("/{creator_id}")
def creator_profile(
    creator_id: int
):

    creator = get_creator(
        creator_id
    )

    if creator is None:

        raise HTTPException(
            status_code=404,
            detail="Creator not found."
        )

    return {
        "success": True,
        "creator": creator
    }