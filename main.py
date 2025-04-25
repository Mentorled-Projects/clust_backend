from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import base
from core.config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS] or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(base.router)

# Healthcheck endpoint
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
