import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.api.routes import router

app = FastAPI(title="RuleGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(router, prefix="/api")
app.include_router(router)

# Resolve frontend dist directory
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

if os.path.isdir(FRONTEND_DIR):
    assets_dir = os.path.join(FRONTEND_DIR, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/")
    async def root():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "RuleGuard API is running"}

    @app.get("/{full_path:path}")
    async def serve_static(full_path: str):
        # Don't intercept API paths
        if full_path.startswith("api/") or full_path in ("query", "health", "sources"):
            raise HTTPException(status_code=404, detail="Not Found")

        # Serve static file if it exists (e.g. favicon, svg)
        direct = os.path.join(FRONTEND_DIR, full_path)
        if os.path.isfile(direct):
            return FileResponse(direct)

        # Fallback to index.html for SPA routing
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)

        return {"message": "RuleGuard API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
