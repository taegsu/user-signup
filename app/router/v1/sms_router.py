from fastapi import APIRouter


router = APIRouter(prefix="/sms/v1")


@router.get(path="/healthcheck")
def healthcheck():
    return {"result": "success"}
