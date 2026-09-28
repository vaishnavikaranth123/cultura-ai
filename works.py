from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
    HTTPException,
)

from backend.config import (
    MAX_UPLOAD_BYTES,
    UPLOAD_DIR,
)

from backend.models.schemas import WorkCreate

from backend.database.database import (
    create_work,
    get_creator,
    get_works,
)


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    prefix="/api/works",
    tags=["Creative Works"],
)


# ==========================================
# ALLOWED IMAGE TYPES
# ==========================================

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


# ==========================================
# CREATE / PUBLISH WORK
# ==========================================

@router.post("/create")
async def create_creator_work(

    creator_id: int = Form(...),

    title: str = Form(...),

    category: str = Form("Art"),

    creator_description: str = Form(""),

    cultural_context: str = Form(""),

    tags: str = Form(""),

    image: UploadFile | None = File(None),

):

    # --------------------------------------
    # Check creator
    # --------------------------------------

    creator = get_creator(
        creator_id
    )

    if creator is None:

        raise HTTPException(
            status_code=404,
            detail="Creator not found.",
        )


    # --------------------------------------
    # Check title
    # --------------------------------------

    if not title.strip():

        raise HTTPException(
            status_code=400,
            detail="Work title is required.",
        )


    image_path = ""


    # --------------------------------------
    # Upload image
    # --------------------------------------

    if image:

        if image.content_type not in ALLOWED_TYPES:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG and WEBP "
                    "images are supported."
                ),
            )


        image_bytes = await image.read()


        if len(image_bytes) > MAX_UPLOAD_BYTES:

            raise HTTPException(
                status_code=413,
                detail=(
                    "Image is larger than the "
                    "maximum allowed size."
                ),
            )


        # Safe filename
        original_name = (
            image.filename or "creative_work"
        )


        safe_name = Path(
            original_name
        ).name.replace(
            " ",
            "_",
        )


        destination = (
            UPLOAD_DIR / safe_name
        )


        # Save image
        with open(
            destination,
            "wb",
        ) as file:

            file.write(
                image_bytes
            )


        image_path = (
            f"/uploads/{safe_name}"
        )


    # --------------------------------------
    # Convert tags
    # --------------------------------------

    tag_list = [

        tag.strip()

        for tag in tags.split(",")

        if tag.strip()

    ]


    # --------------------------------------
    # Create Work object
    # --------------------------------------

    work_data = WorkCreate(

        creator_id=creator_id,

        title=title,

        category=category,

        creator_description=
            creator_description,

        cultural_context=
            cultural_context,

        tags=tag_list,

    )


    # --------------------------------------
    # Save to database
    # --------------------------------------

    work_id = create_work(
        work_data,
        image_path,
    )


    return {

        "success": True,

        "work_id": work_id,

        "message":
            "Creative work published successfully.",

    }


# ==========================================
# GET ALL WORKS
# ==========================================

@router.get("/")
def list_works():

    works = get_works()

    return {

        "success": True,

        "works": works,

    }