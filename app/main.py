from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router

app = FastAPI(title="BOQ Excel Extractor", version="2.0")

# ─── CORS (allow local dev) ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── API routes ───
app.include_router(router)

# ─── Static files ───
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def serve_frontend():
    return FileResponse("app/static/index.html")