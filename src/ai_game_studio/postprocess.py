"""Post-processing transforms applied to generated sprite PNG bytes."""

from io import BytesIO

import rembg
from PIL import Image


def resize_to(image_bytes: bytes, width: int, height: int) -> bytes:
    with Image.open(BytesIO(image_bytes)) as img:
        resized = img.resize((width, height), Image.Resampling.LANCZOS)
        buf = BytesIO()
        resized.save(buf, format="PNG")
        return buf.getvalue()


def remove_background(image_bytes: bytes) -> bytes:
    return rembg.remove(image_bytes)
