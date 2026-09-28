from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .db import init_db
from .routes.auth_routes import router as auth_router
from .template_engine import templates
from .routes.pages import router as page_router
from .routes.planner_routes import router as planner_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app=FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
init_db()
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:8000","http://localhost:8000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
app.include_router(auth_router)
app.include_router(page_router)
app.include_router(planner_router)

@app.get("/health")
def health(): return {"status":"ok","gemini_configured":bool(settings.gemini_api_key),"demo_mode":settings.demo_mode}

@app.get("/startup")
def startup(): return {"status":"initialized","message":"PocketSmart AI is ready"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
