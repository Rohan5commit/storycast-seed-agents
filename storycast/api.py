from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from storycast.config import get_settings
from storycast.pipeline import StoryCastPipeline

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"

app = FastAPI(title="StoryCast", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

JOBS: dict[str, dict[str, Any]] = {}


class CreateStoryCastRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=180)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "examples": [
                "the death of a star",
                "how coral reefs talk to each other",
                "what happens inside a black hole",
            ],
        },
    )


@app.post("/api/storycasts")
def create_storycast(payload: CreateStoryCastRequest, background_tasks: BackgroundTasks) -> dict[str, Any]:
    job_id = uuid4().hex[:12]
    JOBS[job_id] = {
        "job_id": job_id,
        "topic": payload.topic,
        "status": "queued",
        "messages": ["Job accepted"],
    }
    background_tasks.add_task(_run_storycast_job, job_id, payload.topic)
    return JOBS[job_id]


@app.get("/api/storycasts/{job_id}")
def get_storycast(job_id: str) -> dict[str, Any]:
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    response = dict(job)
    if response.get("status") == "completed":
        response["final_video_url"] = f"/media/{job_id}/storycast_final.mp4"
    return response


@app.get("/media/{job_id}/{relative_path:path}")
def get_media(job_id: str, relative_path: str) -> FileResponse:
    job = JOBS.get(job_id)
    if not job or not job.get("run_dir"):
        raise HTTPException(status_code=404, detail="Media job not found")
    run_dir = Path(job["run_dir"]).resolve()
    target = (run_dir / relative_path).resolve()
    if run_dir not in target.parents and target != run_dir:
        raise HTTPException(status_code=403, detail="Invalid media path")
    if not target.exists():
        raise HTTPException(status_code=404, detail="Media file not found")
    return FileResponse(target)


def _run_storycast_job(job_id: str, topic: str) -> None:
    JOBS[job_id]["status"] = "running"

    def progress(message: str) -> None:
        JOBS[job_id].setdefault("messages", []).append(message)

    try:
        pipeline = StoryCastPipeline(get_settings())
        manifest = pipeline.run(topic, progress_callback=progress)
        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["run_dir"] = manifest.run_dir
        JOBS[job_id]["manifest"] = manifest.model_dump(mode="json")
    except Exception as exc:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(exc)
