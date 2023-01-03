import json
from functools import lru_cache

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
