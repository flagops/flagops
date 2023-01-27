from fastapi import FastAPI
from ..common.config import get_settings
from ..common.utils import get_buildinfo
from .admin.router import router as admin_router

app = FastAPI()

app.include_router(
    admin_router,
    prefix="/admin",
    tags=["admin"]
)

@app.get('/')
def index():
    return get_settings().dict()

@app.get('/buildinfo')
def buildinfo():
    return get_buildinfo()
