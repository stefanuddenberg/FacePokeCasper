"""
Sync Python API for FacePoke, for notebooks and scripts.

Wraps Engine.load_image / Engine.transform_image without the WebSocket server.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import io
from pathlib import Path
from typing import Dict, Optional, Union

from PIL import Image

from engine import Engine
from loader import initialize_models

ImageInput = Union[str, Path, bytes, Image.Image]

PARAM_NAMES = (
    "smile",
    "aaa",
    "eee",
    "woo",
    "wink",
    "pupil_x",
    "pupil_y",
    "eyes",
    "eyebrow",
    "rotate_pitch",
    "rotate_yaw",
    "rotate_roll",
)


def _run(coro):
    """Run an async coroutine from sync code, including inside Jupyter."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


def _to_bytes(image: ImageInput) -> bytes:
    if isinstance(image, bytes):
        return image
    if isinstance(image, (str, Path)):
        return Path(image).read_bytes()
    if isinstance(image, Image.Image):
        buf = io.BytesIO()
        rgb = image.convert("RGB")
        rgb.save(buf, format="PNG")
        return buf.getvalue()
    raise TypeError(f"Unsupported image type: {type(image)!r}")


class FacePoke:
    """Load a face once, then apply expression/pose params repeatedly."""

    def __init__(self, engine: Optional[Engine] = None):
        if engine is None:
            live_portrait = _run(initialize_models())
            engine = Engine(live_portrait)
        self.engine = engine
        self._uid: Optional[str] = None
        self.meta: Optional[Dict] = None

    def load(self, image: ImageInput) -> Dict:
        """Load and cache a face image. Accepts a path, bytes, or PIL.Image."""
        data = _to_bytes(image)
        meta = _run(self.engine.load_image(data))
        self._uid = meta["u"]
        self.meta = meta
        return meta

    def transform(self, **params: float) -> Image.Image:
        """
        Apply FacePoke params and return a PIL image.

        Supported kwargs: smile, aaa, eee, woo, wink, pupil_x, pupil_y,
        eyes, eyebrow, rotate_pitch, rotate_yaw, rotate_roll.
        """
        if self._uid is None:
            raise RuntimeError("Call load() before transform()")
        unknown = set(params) - set(PARAM_NAMES)
        if unknown:
            raise ValueError(f"Unknown params: {sorted(unknown)}")
        webp = _run(self.engine.transform_image(self._uid, dict(params)))
        return Image.open(io.BytesIO(webp)).convert("RGB")
