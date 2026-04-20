"""Compose multiple frame PNGs into a single grid-layout spritesheet PNG."""

from io import BytesIO

from PIL import Image


def build_spritesheet(frames: list[bytes], columns: int) -> bytes:
    if not frames:
        raise ValueError("frames must not be empty")
    if columns < 1:
        raise ValueError("columns must be >= 1")

    images = [Image.open(BytesIO(f)) for f in frames]
    try:
        frame_width, frame_height = images[0].size
        for img in images[1:]:
            if img.size != (frame_width, frame_height):
                raise ValueError("all frames must share identical dimensions")

        rows = (len(images) + columns - 1) // columns
        sheet = Image.new(
            "RGBA",
            (frame_width * columns, frame_height * rows),
            (0, 0, 0, 0),
        )
        for index, img in enumerate(images):
            x = (index % columns) * frame_width
            y = (index // columns) * frame_height
            sheet.paste(img, (x, y))

        buf = BytesIO()
        sheet.save(buf, format="PNG")
        return buf.getvalue()
    finally:
        for img in images:
            img.close()
