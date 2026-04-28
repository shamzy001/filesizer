from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .fileops import ConflictError, PathError, delete_item, move_item
from .scanner import scan_directory_async

app = FastAPI(title="filesizer")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(127\.0\.0\.1|localhost)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/scan")
async def api_scan(path: str = Query(...), depth: Optional[int] = Query(None)):
    p = Path(path)
    if not p.exists() or not p.is_dir():
        raise HTTPException(status_code=400, detail=f"Not a valid directory: {path}")
    return await scan_directory_async(str(p), max_depth=depth)


class DeleteRequest(BaseModel):
    path: str
    root: str
    permanent: bool = False


class MoveRequest(BaseModel):
    source: str
    destination: str
    root: str


@app.post("/api/delete")
async def api_delete(req: DeleteRequest):
    try:
        delete_item(req.path, req.root, req.permanent)
    except PathError:
        raise HTTPException(status_code=403, detail="Path is outside the allowed root")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"status": "ok"}


@app.post("/api/move")
async def api_move(req: MoveRequest):
    try:
        move_item(req.source, req.destination, req.root)
    except PathError:
        raise HTTPException(status_code=403, detail="Path is outside the allowed root")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return {"status": "ok"}


# Static files mount last so API routes take priority
_static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(_static_dir), html=True), name="static")
