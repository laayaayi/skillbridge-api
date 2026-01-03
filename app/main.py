from fastapi import FastAPI
from app.routers.skills import router as skills_router

from app.routers.users import router as users_router
from app.database import Base, engine
import app.models  # noqa: F401
from app.routers.auth import router as auth_router
from app.routers.tasks import router as tasks_router

app = FastAPI(title="SkillBridge API", version="0.1.0")

# Create tables (dev: sqlite)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(skills_router)
app.include_router(tasks_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "skillbridge-api"}
