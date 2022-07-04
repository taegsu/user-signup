from fastapi import APIRouter


router = APIRouter(prefix="/user/v1")


@router.get(path="/healthcheck")
def healthcheck():
    return {"result": "success"}
