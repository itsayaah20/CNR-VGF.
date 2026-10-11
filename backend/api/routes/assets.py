from fastapi import APIRouter

router = APIRouter()


@router.get("/assets")
def assets():

    return {
        "message": "assets endpoint"
    }