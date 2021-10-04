from typing import List
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.db import init_db, SessionLocal
from app.api.v1 import api_router
from app.config import get_settings
settings = get_settings()

db = SessionLocal()
init_db(db)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.mount("/upload", StaticFiles(directory=settings.STATIC_FILES), name="upload")