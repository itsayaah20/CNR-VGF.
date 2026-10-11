from fastapi import FastAPI
from backend.api.routes.advisor import router as advisor_router

app = FastAPI(
    title="CNR-VGF",
    version="1.0.0"
)

app.include_router(advisor_router)

@app.get("/")
def root():

    return {
        "application": "Cyber Net Risk Framework",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

from fastapi import FastAPI

from backend.api.routes.health import router as health_router
from backend.api.routes.advisor import router as advisor_router
from backend.api.routes.assets import router as assets_router
from backend.api.routes.vulnerabilities import (
    router as vulnerabilities_router
)

app = FastAPI(
    title="CNR-VGF"
)

app.include_router(health_router)
app.include_router(advisor_router)
app.include_router(assets_router)
app.include_router(vulnerabilities_router)


@app.get("/")
def root():

    return {
        "message": "CNR-VGF API"
    }