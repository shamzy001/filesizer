# filesizer

Browser-based file size visualizer. Pick a directory, see a sorted breakdown of disk usage, navigate the tree, and delete or move items — all from a local browser window.

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
