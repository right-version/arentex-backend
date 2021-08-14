from typing import List
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from app.db import init_db, SessionLocal
from app.api.v1 import api_router
from app.config import get_settings
settings = get_settings()

db = SessionLocal()
init_db(db)

app = FastAPI()
app.include_router(api_router)
app.mount("/upload", StaticFiles(directory=settings.STATIC_FILES), name="upload")