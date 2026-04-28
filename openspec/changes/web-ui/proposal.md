## Why

There is currently no way to visualize disk usage for a selected directory. This change introduces a browser-based UI that lets users explore directory trees by size, navigate into subdirectories, and perform file management operations (delete, move) — all from a local web interface.

## What Changes

- A local HTTP server (Python backend) that exposes a REST API for scanning directories and performing file operations
- A browser-based frontend that renders an interactive size visualization (treemap or sortable list) for a chosen directory
- Directory navigation allowing the user to drill into subdirectories
- File/directory delete and move operations triggered from the UI
- A launcher entry point (`filesizer`) that starts the local server and opens the browser automatically

## Capabilities

### New Capabilities

- `directory-scanner`: Recursively scan a directory tree, compute sizes for all files and directories, and return structured results
- `file-operations`: Delete or move files and directories from the backend, with safety checks
- `web-server`: Local HTTP server that serves the frontend and exposes REST API endpoints
- `size-visualization`: Browser UI rendering file/directory sizes as a navigable, sortable view (treemap or list)

### Modified Capabilities

## Impact

- New Python dependencies: a lightweight web framework (e.g., FastAPI or Flask), possibly `uvicorn` for ASGI serving
- New frontend assets (HTML/CSS/JS or a small JS framework)
- `pyproject.toml` and project package structure must be established
- No external network access required — entirely local