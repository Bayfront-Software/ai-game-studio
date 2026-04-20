"""Unit tests for the core sprite generation orchestration."""

from pathlib import Path

from ai_game_studio.sprite_gen import generate_sprite


class FakeGenerator:
    def __init__(self, image_bytes: bytes) -> None:
        self._bytes = image_bytes

    def generate(self, prompt: str) -> bytes:
        return self._bytes


def test_generate_sprite_writes_bytes_to_output_path(tmp_path: Path) -> None:
    fake = FakeGenerator(b"fake-png-bytes")
    output = tmp_path / "sprite.png"

    result = generate_sprite("a hero with a sword", output, generator=fake)

    assert result == output
    assert output.read_bytes() == b"fake-png-bytes"


def test_generate_sprite_applies_post_processors_in_order(tmp_path: Path) -> None:
    fake = FakeGenerator(b"raw")
    output = tmp_path / "sprite.png"

    def append_a(image_bytes: bytes) -> bytes:
        return image_bytes + b"-a"

    def append_b(image_bytes: bytes) -> bytes:
        return image_bytes + b"-b"

    generate_sprite(
        "prompt",
        output,
        generator=fake,
        post_processors=[append_a, append_b],
    )

    assert output.read_bytes() == b"raw-a-b"
