"""Core sprite generation orchestration: delegates image synthesis to an injected generator, applies optional post-processors, and persists the result."""

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Protocol


class ImageGenerator(Protocol):
    def generate(self, prompt: str) -> bytes: ...


PostProcessor = Callable[[bytes], bytes]


def generate_sprite(
    prompt: str,
    output_path: Path,
    *,
    generator: ImageGenerator,
    post_processors: Sequence[PostProcessor] = (),
) -> Path:
    image_bytes = generator.generate(prompt)
    for processor in post_processors:
        image_bytes = processor(image_bytes)
    output_path.write_bytes(image_bytes)
    return output_path
