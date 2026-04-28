## Context

filesizer is a new Python project with no existing source code. The goal is to build a local tool that lets a user pick a directory, see a visual breakdown of disk usage, navigate the tree, and delete or move items — all from a browser window. The tool runs entirely on the user's machine; no network access or authentication is needed.

## Goals / Non-Goals

**Goals:**
- Launch a local HTTP server from a single CLI command (`filesizer [path]`)
- Serve a browser UI that shows files/folders sorted and sized visually
- Allow drill-down navigation into subdirectories
- Support delete and move operations via the UI
- Keep the stack simple and self-contained (no Node.js build step required at runtime)

**Non-Goals:**
- Cloud storage or remote file systems
- Multi-user access or authentication
- Real-time file system watching / auto-refresh
- Packaging as a native desktop app (Electron, etc.)
- Support for Windows symlink loops beyond basic cycle detection

## Decisions

### Backend: FastAPI + uvicorn
**Decision**: Use FastAPI (with uvicorn) as the local HTTP server.  
**Rationale**: FastAPI provides automatic JSON serialization, async support for non-blocking directory scans, and clean path parameter routing. It ships as a single `pip install fastapi uvicorn` with no system dependencies.  
**Alternatives considered**:  
- Flask: simpler but synchronous; large directory scans would block the server thread.  
- http.server (stdlib): too low-level; no routing or async.

### Frontend: Vanilla JS + single HTML file
**Decision**: Ship a single `index.html` with inline or co-located JS/CSS. No build toolchain.  
**Rationale**: Keeps the project dependency-free on the frontend side. The UI can be served directly from FastAPI's static file handler. A treemap can be rendered with a small canvas-based library (e.g., `squarify` logic in JS, or D3's `treemap` loaded from CDN).  
**Alternatives considered**:  
- React/Vue SPA: adds a build step (npm, webpack) that complicates installation for a Python-first tool.  
- Streamlit: opinionated layout, limited file tree UX.

### Directory scanning: synchronous with async wrapper
**Decision**: Use `os.scandir` recursively in a thread pool (`asyncio.to_thread`) so the FastAPI event loop stays responsive.  
**Rationale**: `os.scandir` is the fastest stdlib option for directory traversal. Wrapping it in `asyncio.to_thread` keeps the API non-blocking so the browser can show a loading state.  
**Alternatives considered**:  
- `pathlib.Path.rglob`: cleaner API but slightly slower; no meaningful difference for this use case.  
- `shutil.disk_usage`: only gives totals, not per-item breakdown.

### File operations: server-side with confirmation
**Decision**: Delete uses `send2trash` (recycle bin) by default; move uses `shutil.move`. Both require an explicit confirmation payload from the frontend.  
**Rationale**: `send2trash` prevents accidental permanent deletion, which matters for a local tool where undo is expected. `shutil.move` handles cross-device moves.  
**Alternatives considered**:  
- `os.remove` / `shutil.rmtree`: permanent, no recovery — too risky as default.

### Project layout: `src/` layout with `pyproject.toml`
**Decision**: Use a `src/filesizer/` package with `pyproject.toml` (PEP 517).  
**Rationale**: Prevents accidental imports of the uninstalled package during development; aligns with modern Python packaging best practices.

## Risks / Trade-offs

- **Large directories** → scan can take seconds for very deep or large trees. Mitigation: stream results progressively or return a depth-limited initial scan with lazy expansion.
- **Path traversal in API** → malicious input could escape the scanned root. Mitigation: resolve all paths server-side and reject any path that doesn't start with the declared root.
- **send2trash not available on all platforms** → fall back to `os.remove`/`shutil.rmtree` with an explicit "permanent delete" warning in the UI.
- **Browser CORS** → since server and browser are both localhost this is a non-issue, but FastAPI CORS middleware will be configured to allow only `127.0.0.1`.