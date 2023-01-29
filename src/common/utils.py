from typing import Union
from pydantic import UUID4
import json
import jwt
from fastapi import Header, HTTPException, status
from functools import lru_cache
from .config import async_sessionmaker
from .jwk_client import get_jwk_client

async def get_db_session():
    db = async_sessionmaker()
    try:
        yield db
    finally:
        await db.close()

@lru_cache()
def get_buildinfo():
    try:
        with open("build_info.json", "r") as f:
            ret = json.load(f)
        return ret
    except FileNotFoundError:
        return {
            "error": "BuildInfoNotFound"
        }
    except json.JSONDecodeError:
        return {
            "error": "BuildInfoFormatError"
        }

async def validate_token(authorization: str = Header(default=None))->UUID4:
    jwk_client = get_jwk_client()
    if authorization:
        token = authorization.strip().split(" ")[1]
        key, algs = await jwk_client.get_key_and_algorithms(token)
        try:
            payload = jwt.decode(token, key=key, algorithms=algs, options={"verify_exp": False, "verify_aud": False})
            return UUID4(payload["tenantId"])
        except jwt.exceptions.InvalidTokenError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization token")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
