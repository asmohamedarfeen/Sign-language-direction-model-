"""
FastAPI Main Application Entrypoint.

Registers CORS, exception handlers, lifecycle events, and feature routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import engine, Base, AsyncSessionLocal
from backend.core.logging import logger
from backend.core.exceptions import (
    SignSpeakException,
    signspeak_exception_handler,
    generic_exception_handler,
)
from backend.recognition.routes import router as recognition_router
from backend.vocabulary.routes import router as vocabulary_router
from backend.history.routes import router as history_router
from backend.recognition.service.recognition_service import RecognitionService
from backend.vocabulary.repository.sign_repository import SignRepository
from backend.vocabulary.service.sign_service import SignService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle startup and shutdown handler."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}...")

    # 1. Initialize Database Tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schema verified.")

    # 2. Seed Default Vocabulary if empty
    async with AsyncSessionLocal() as session:
        sign_repo = SignRepository(session)
        sign_service = SignService(sign_repo)
        await sign_service.seed_default_signs()
        await session.commit()

    # 3. Pre-load ML Model
    try:
        RecognitionService.get_model()
        logger.info("Sign language recognition model ready.")
    except Exception as e:
        logger.warning(f"Model pre-warm warning: {e}. Model will load upon training/weight availability.")

    yield

    # Shutdown
    await engine.dispose()
    logger.info("Application shutdown complete.")


# Initialize FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production Sign Language to English Translation Engine",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Exception Handlers
app.add_exception_handler(SignSpeakException, signspeak_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Register Feature Routers
app.include_router(recognition_router, prefix=settings.API_V1_PREFIX)
app.include_router(vocabulary_router, prefix=settings.API_V1_PREFIX)
app.include_router(history_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
@app.get(f"{settings.API_V1_PREFIX}/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health_check():
    """Returns application health and model availability."""
    model_loaded = False
    try:
        RecognitionService.get_model()
        model_loaded = True
    except Exception:
        pass

    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model_loaded": model_loaded
    }


@app.get("/", tags=["Root"])
async def root():
    """Root info endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs_url": "/docs",
        "health_url": f"{settings.API_V1_PREFIX}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
