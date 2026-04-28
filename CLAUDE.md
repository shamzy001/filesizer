# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**filesizer** — a browser-based disk usage visualizer. Launch from the command line, pick a directory, and get a sorted breakdown of disk usage with the ability to delete or move items from a local browser window.

## Stack

- **Backend**: Python 3.11+, FastAPI, uvicorn
- **Frontend**: Single-file vanilla JS/HTML (`src/filesizer/static/index.html`) — no build step
- **File ops**: `send2trash` for safe (trash-based) deletion; `shutil` for permanent delete and move
- **Tests**: pytest + pytest-asyncio + httpx

## Architecture

| Module | Responsibility |
|--------|---------------|
| `cli.py` | Entry point — argument parsing, launches uvicorn, opens browser |
| `scanner.py` | Recursive directory scan with async wrapper; cycle detection via symlink resolution |
| `fileops.py` | `delete_item` and `move_item` with path validation (prevents escaping root) |
| `server.py` | FastAPI app — `/api/scan`, `/api/delete`, `/api/move` endpoints |
| `static/index.html` | Full frontend — dark theme, directory tree, size bars |

## Running Locally

```bash
pip install -e ".[dev]"
python -m filesizer              # directory picker on launch
python -m filesizer /some/path   # jump straight to a directory
```

Server starts at `http://127.0.0.1:8765` (auto-increments port if taken) and opens the browser automatically.

## Running Tests

```bash
python -m pytest
```

## Known Issues

- **Delete does not work** — the `/api/delete` endpoint and `fileops.delete_item` backend logic appear correct, but the delete action triggered from the frontend does not successfully remove items. The bug is likely in how the frontend constructs or sends the delete request (`static/index.html`). Needs investigation.

## Design

This project was designed using [OpenSpec](https://openspec.dev) for structured specification and built with [Claude Code](https://claude.ai/code). Design documents and feature specs are in the `openspec/` directory.
