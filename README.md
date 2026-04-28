# filesizer

Browser-based file size visualizer. Pick a directory, see a sorted breakdown of disk usage, navigate the tree, and delete or move items — all from a local browser window.

## Features

- Recursive directory scan with real-time size bars
- Navigate into subdirectories and back
- Delete items (moved to trash via `send2trash`) or move them elsewhere
- Handles symlink cycles and permission errors gracefully
- Dark theme, no external service dependencies

## Requirements

- Python 3.11+

## Installation

```bash
pip install -e .
```

For development (includes test dependencies):

```bash
pip install -e ".[dev]"
```

## Usage

Launch with a directory picker:

```bash
python -m filesizer
```

Launch and jump straight to a directory:

```bash
python -m filesizer /path/to/directory
```

The server starts on `http://127.0.0.1:8765` (or the next available port) and opens your browser automatically.

## Running Tests

```bash
python -m pytest
```

## Known Issues

- **Delete is currently broken** — the backend logic is in place but the delete action from the UI does not work correctly. Fix in progress.

## Design & Development

This project was designed using [OpenSpec](https://openspec.dev) for structured feature specification and built with [Claude Code](https://claude.ai/code). Feature specs and design documents are available in the `openspec/` directory.
