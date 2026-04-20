"""Tests for sprite post-processing transforms."""

from io import BytesIO
from unittest.mock import patch

from PIL import Image

from ai_game_studio.postprocess import remove_background, resize_to


def _make_solid_png(width: int, height: int) -> bytes:
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_resize_to_produces_image_with_specified_dimensions() -> None:
    original = _make_solid_png(512, 512)

    resized = resize_to(original, 64, 64)

    with Image.open(BytesIO(resized)) as img:
        assert img.size == (64, 64)


def test_remove_background_delegates_to_rembg_remove() -> None:
    input_bytes = b"input-png"
    output_bytes = b"transparent-png"

    with patch(
        "ai_game_studio.postprocess.rembg.remove",
        return_value=output_bytes,
    ) as mock_remove:
        result = remove_background(input_bytes)

    assert result == output_bytes
    mock_remove.assert_called_once_with(input_bytes)
