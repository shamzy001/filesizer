from __future__ import annotations

import logging
import os
import shutil

logger = logging.getLogger(__name__)

_SEND2TRASH_AVAILABLE = True
try:
    import send2trash as _send2trash  # type: ignore[import-untyped]
except ImportError:
    _SEND2TRASH_AVAILABLE = False


class PathError(ValueError):
    pass


class ConflictError(FileExistsError):
    pass


def validate_path(path: str, root: str) -> str:
    """Resolve path to absolute and verify it is within root. Returns resolved path."""
    resolved = os.path.realpath(os.path.abspath(path))
    resolved_root = os.path.realpath(os.path.abspath(root))
    if resolved != resolved_root and not resolved.startswith(resolved_root + os.sep):
        raise PathError(f"Path {resolved!r} is outside root {resolved_root!r}")
    return resolved


def delete_item(path: str, root: str, permanent: bool = False) -> None:
    resolved = validate_path(path, root)
    if not os.path.exists(resolved):
        raise FileNotFoundError(f"Path not found: {resolved}")

    if _SEND2TRASH_AVAILABLE and not permanent:
        _send2trash.send2trash(resolved)
        return

    if not _SEND2TRASH_AVAILABLE and not permanent:
        raise RuntimeError(
            "send2trash is not available; set permanent=true to confirm permanent deletion"
        )

    if os.path.isdir(resolved):
        shutil.rmtree(resolved)
    else:
        os.remove(resolved)


def move_item(source: str, destination: str, root: str) -> None:
    resolved_src = validate_path(source, root)
    resolved_dst = validate_path(destination, root)

    if not os.path.exists(resolved_src):
        raise FileNotFoundError(f"Source not found: {resolved_src}")

    final_dst = (
        os.path.join(resolved_dst, os.path.basename(resolved_src))
        if os.path.isdir(resolved_dst)
        else resolved_dst
    )
    if os.path.exists(final_dst):
        raise ConflictError(f"Destination already exists: {final_dst}")

    shutil.move(resolved_src, resolved_dst)