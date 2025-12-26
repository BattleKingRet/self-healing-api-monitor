from fastapi import FastAPI
from app.api.ingest import router as ingest_router
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger("app")

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0"
)

@app.get("/health")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok", "env": settings.ENV}

app.include_router(ingest_router, prefix="/api")
