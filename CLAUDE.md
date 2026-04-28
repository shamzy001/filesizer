# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**filesizer** — a Python application for visualizing file and folder sizes on disk, with options to delete or move them.

## Status

This project is in early development. No source code, dependencies, or build tooling exist yet. The `.idea/filesizer.iml` confirms it is configured as a Python module in IntelliJ IDEA.

## Getting Started

When adding code, establish the project structure first:

- Use a `src/` or flat layout with a top-level package named `filesizer`
- Add `requirements.txt` or `pyproject.toml` for dependencies
- Add a `README.md` with setup and usage instructions once the stack is decided

## Architecture Intent

The application needs to:
1. Scan a directory tree and compute sizes recursively
2. Present a navigable view of files/folders sorted or grouped by size
3. Allow the user to delete or move selected items
