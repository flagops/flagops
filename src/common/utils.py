import json
from functools import lru_cache
from .config import async_sessionmaker

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
