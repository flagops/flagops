from functools import lru_cache
import aiohttp
import jwt
from jwt import PyJWK
from .config import get_settings

class JWKClient:
    def __init__(self, url):
        self.jwks_url = url
        self.keys = {}

    async def fetch_keys_from_jwks_endpoint(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.jwks_url) as response:
                try:
                    res = await response.json()
                    return res["keys"]
                except:
                    return []

    async def get_key_by_kid(self, kid):
        if kid in self.keys:
            return self.keys[kid]
        else:
            keys_list = await self.fetch_keys_from_jwks_endpoint()
            for key in keys_list:
                self.keys[key["kid"]] = key
            if kid in self.keys:
                return self.keys[kid]
            else:
                return None

    async def get_key_and_algorithms(self, token):
        headers = jwt.get_unverified_header(token)
        kid = headers["kid"]
        key_dict = await self.get_key_by_kid(kid)
        key_obj = PyJWK(key_dict)
        return (key_obj.key, [key_dict["alg"]])
        
@lru_cache()
def get_jwk_client():
    settings = get_settings()
    return JWKClient(settings.jwks_url)
