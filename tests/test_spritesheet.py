"""Tests for assembling a spritesheet from a list of frame PNG bytes."""

from io import BytesIO

from PIL import Image

from ai_game_studio.spritesheet import build_spritesheet


def _make_solid_png(width: int, height: int, color: tuple[int, int, int]) -> bytes:
    img = Image.new("RGB", (width, height), color=color)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_build_spritesheet_output_has_cols_x_rows_of_frame_dimensions() -> None:
    frame_width, frame_height = 32, 48
    frames = [_make_solid_png(frame_width, frame_height, (255, 0, 0)) for _ in range(4)]

    sheet_bytes = build_spritesheet(frames, columns=2)

    with Image.open(BytesIO(sheet_bytes)) as sheet:
        assert sheet.size == (frame_width * 2, frame_height * 2)


def test_build_spritesheet_places_frames_left_to_right_top_to_bottom() -> None:
    red = _make_solid_png(16, 16, (255, 0, 0))
    green = _make_solid_png(16, 16, (0, 255, 0))
    blue = _make_solid_png(16, 16, (0, 0, 255))
    yellow = _make_solid_png(16, 16, (255, 255, 0))

    sheet_bytes = build_spritesheet([red, green, blue, yellow], columns=2)

    with Image.open(BytesIO(sheet_bytes)) as sheet:
        rgba_sheet = sheet.convert("RGBA")
        assert rgba_sheet.getpixel((0, 0))[:3] == (255, 0, 0)
        assert rgba_sheet.getpixel((16, 0))[:3] == (0, 255, 0)
        assert rgba_sheet.getpixel((0, 16))[:3] == (0, 0, 255)
        assert rgba_sheet.getpixel((16, 16))[:3] == (255, 255, 0)
