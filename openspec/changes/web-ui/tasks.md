## 1. Project Setup

- [x] 1.1 Create `pyproject.toml` with project metadata, dependencies (fastapi, uvicorn, send2trash), and a `filesizer` CLI entry point
- [x] 1.2 Create `src/filesizer/__init__.py` and `src/filesizer/__main__.py` (package entry point)
- [x] 1.3 Create `src/filesizer/static/` directory to hold frontend assets
- [x] 1.4 Create `README.md` with installation and usage instructions

## 2. Directory Scanner

- [x] 2.1 Implement `src/filesizer/scanner.py` with a recursive `scan_directory(path, max_depth=None)` function using `os.scandir`
- [x] 2.2 Add cycle detection for symlinks (track visited inode/device pairs)
- [x] 2.3 Wrap the synchronous scan in `asyncio.to_thread` for non-blocking use in FastAPI
- [x] 2.4 Define a `ScanNode` dataclass/TypedDict with `name`, `path`, `size`, `is_dir`, `children`, `truncated` fields

## 3. File Operations

- [x] 3.1 Implement `src/filesizer/fileops.py` with a `delete_item(path, root, permanent=False)` function
- [x] 3.2 Add `send2trash` usage in `delete_item` with fallback to permanent delete when unavailable
- [x] 3.3 Implement `move_item(source, destination, root)` using `shutil.move`
- [x] 3.4 Implement `validate_path(path, root)` that resolves absolute paths and raises if outside root

## 4. Web Server

- [x] 4.1 Implement `src/filesizer/server.py` with a FastAPI app, CORS restricted to localhost
- [x] 4.2 Add `GET /api/scan` endpoint with `path` and `depth` query parameters
- [x] 4.3 Add `POST /api/delete` endpoint accepting `{"path": str, "permanent": bool}` JSON body
- [x] 4.4 Add `POST /api/move` endpoint accepting `{"source": str, "destination": str}` JSON body
- [x] 4.5 Mount `src/filesizer/static/` as a StaticFiles route; serve `index.html` at `GET /`
- [x] 4.6 Implement port-fallback logic in the startup routine (try 8765, then next available)

## 5. CLI Entry Point

- [x] 5.1 Implement `src/filesizer/cli.py` with argument parsing (`filesizer [path]`)
- [x] 5.2 Start uvicorn programmatically from `cli.py`
- [x] 5.3 Open the browser automatically using `webbrowser.open` after server starts

## 6. Frontend — Size Visualization

- [x] 6.1 Create `src/filesizer/static/index.html` with a path input form and scan button
- [x] 6.2 Add a sortable list view rendering each item's name, human-readable size, and proportional size bar
- [x] 6.3 Implement breadcrumb navigation component that updates on drill-down and supports clicking ancestors
- [x] 6.4 Wire directory-click events to re-fetch `/api/scan` for the clicked path and re-render
- [x] 6.5 Add a loading spinner shown while scan requests are in flight

## 7. Frontend — File Operations

- [x] 7.1 Add a Delete button per row that shows a confirmation dialog before sending `POST /api/delete`
- [x] 7.2 On successful delete, remove the item from the displayed list without a full re-scan
- [x] 7.3 Add a Move button per row that opens an input dialog for the destination path and sends `POST /api/move`
- [x] 7.4 Display inline error messages for failed delete/move operations (HTTP 403, 404, 409)

## 8. Testing & Validation

- [x] 8.1 Write unit tests for `scanner.py` covering flat dirs, nested dirs, permission errors, and symlink cycles
- [x] 8.2 Write unit tests for `fileops.py` covering delete, move, and path validation edge cases
- [x] 8.3 Write integration tests for each API endpoint using FastAPI's `TestClient`
- [ ] 8.4 Manually verify the browser UI end-to-end: scan, navigate, delete, move
