from __future__ import annotations

import asyncio
import logging
import os
from typing import TypedDict

logger = logging.getLogger(__name__)


class ScanNode(TypedDict):
    name: str
    path: str
    size: int
    is_dir: bool
    children: list[ScanNode]
    truncated: bool


def scan_directory(path: str, max_depth: int | None = None) -> ScanNode:
    visited: set[str] = set()
    return _scan(os.path.abspath(path), max_depth, 0, visited)


def _scan(abs_path: str, max_depth: int | None, depth: int, visited: set[str]) -> ScanNode:
    real_path = os.path.realpath(abs_path)
    name = os.path.basename(abs_path) or abs_path

    try:
        is_dir = os.path.isdir(real_path)
    except OSError as exc:
        logger.warning("Cannot check %s: %s", abs_path, exc)
        return ScanNode(name=name, path=abs_path, size=0, is_dir=False, children=[], truncated=False)

    if not is_dir:
        try:
            size = os.path.getsize(real_path)
        except OSError as exc:
            logger.warning("Cannot stat %s: %s", abs_path, exc)
            size = 0
        return ScanNode(name=name, path=abs_path, size=size, is_dir=False, children=[], truncated=False)

    # Cycle detection via real path — prevents symlink loops and double-counting hardlinks
    if real_path in visited:
        logger.warning("Cycle detected at %s, skipping", abs_path)
        return ScanNode(name=name, path=abs_path, size=0, is_dir=True, children=[], truncated=True)
    visited.add(real_path)

    if max_depth is not None and depth >= max_depth:
        return ScanNode(name=name, path=abs_path, size=0, is_dir=True, children=[], truncated=True)

    children: list[ScanNode] = []
    try:
        entries = list(os.scandir(real_path))
    except PermissionError as exc:
        logger.warning("Cannot read %s: %s", abs_path, exc)
        return ScanNode(name=name, path=abs_path, size=0, is_dir=True, children=[], truncated=False)

    for entry in entries:
        try:
            child = _scan(entry.path, max_depth, depth + 1, visited)
            children.append(child)
        except OSError as exc:
            logger.warning("Skipping %s: %s", entry.path, exc)

    total = sum(c["size"] for c in children)
    return ScanNode(name=name, path=abs_path, size=total, is_dir=True, children=children, truncated=False)


async def scan_directory_async(path: str, max_depth: int | None = None) -> ScanNode:
    return await asyncio.to_thread(scan_directory, path, max_depth)
