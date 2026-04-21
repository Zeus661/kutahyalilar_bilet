from fastapi import HTTPException


def not_found(resource: str):
    raise HTTPException(status_code=404, detail=f"{resource} not found")


def unauthorized():
    raise HTTPException(status_code=401, detail="Unauthorized")


def conflict(msg: str):
    raise HTTPException(status_code=409, detail=msg)


def bad_request(msg: str):
    raise HTTPException(status_code=400, detail=msg)
