from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.upload import router as upload_router
from app.databases.database import engine
from app.databases.models import Base


Base.metadata.create_all(bind=engine)

# Create the FastAPI application instance.
app = FastAPI()

# Enable CORS for the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the upload router so /upload is available on the app.
app.include_router(upload_router)


@app.get("/", response_model=dict)
def read_root():
    """Return a simple JSON greeting at the root endpoint."""
    return {"message": "Welcome to the AI Policy Summarizer API"}


@app.get("/health", response_model=dict)
def read_health():
    """Return a JSON health check response."""
    return {"status": "ok"}
