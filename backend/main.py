from __future__ import annotations

from pathlib import Path

import fastapi
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config.logging_config import configure_logging, logger
from backend.config.settings import settings
from backend.routes.chat import router

configure_logging()

app = fastapi.FastAPI(
    title="Bengoshi by VakilBabu",
    description="Production-ready chatbot backend for VakilBabu",
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="frontend_static")


@app.get("/", include_in_schema=False)
async def serve_frontend() -> FileResponse:
    index_file = frontend_dir / "index.html"
    if not index_file.exists():
        raise FileNotFoundError("Frontend index.html not found.")
    return FileResponse(index_file)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc):
    logger.warning("Validation error: %s", exc)
    return {"detail": exc.errors()}, 400


@app.get("/health")
async def health_root() -> dict:
    return {"status": "ok", "app_name": settings.app_name, "version": settings.app_version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
