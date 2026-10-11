from fastapi import APIRouter

router = APIRouter()


@router.get("/vulnerabilities")
def vulnerabilities():

    return {
        "message": "vulnerabilities endpoint"
    }