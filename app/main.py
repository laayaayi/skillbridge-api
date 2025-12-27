from fastapi import FastAPI

from app.database import Base, engine
import app.models  # noqa: F401
from app.routers.auth import router as auth_router

app = FastAPI(title="SkillBridge API", version="0.1.0")

# Create tables (dev: sqlite)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "skillbridge-api"}
