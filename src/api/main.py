from fastapi import FastAPI
from ..common.config import get_settings
from ..common.utils import get_buildinfo

app = FastAPI()

@app.get('/')
def index():
    return get_settings().dict()

@app.get('/buildinfo')
def buildinfo():
    return get_buildinfo()
