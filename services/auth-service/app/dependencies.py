from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            os.environ["JWT_SECRET_KEY"],
            algorithms=[os.environ.get("JWT_ALGORITHM", "HS256")]
        )
        return {
            "user_id": payload["sub"],
            "email": payload["email"],
            "is_admin": payload.get("is_admin", False)
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
