"""Core sprite generation orchestration: delegates image synthesis to an injected generator and persists the result."""

from pathlib import Path
from typing import Protocol


class ImageGenerator(Protocol):
    def generate(self, prompt: str) -> bytes: ...


def generate_sprite(
    prompt: str,
    output_path: Path,
    *,
    generator: ImageGenerator,
) -> Path:
    image_bytes = generator.generate(prompt)
    output_path.write_bytes(image_bytes)
    return output_path
