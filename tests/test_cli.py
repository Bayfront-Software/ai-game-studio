"""End-to-end tests for the gen-sprite CLI command."""

from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from PIL import Image

from ai_game_studio.cli import main


def _make_solid_png(width: int, height: int) -> bytes:
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_cli_invokes_generator_and_writes_sprite_to_output_path(tmp_path: Path) -> None:
    output_file = tmp_path / "hero.png"
    fake_bytes = b"cli-test-bytes"

    runner = CliRunner()
    with patch("ai_game_studio.cli.FalFluxGenerator") as mock_generator_cls:
        mock_generator_cls.return_value.generate.return_value = fake_bytes

        result = runner.invoke(main, ["a brave hero", "-o", str(output_file)])

    assert result.exit_code == 0, result.output
    assert output_file.read_bytes() == fake_bytes


def test_cli_resizes_sprite_when_size_option_given(tmp_path: Path) -> None:
    output_file = tmp_path / "hero.png"
    generated_png = _make_solid_png(512, 512)

    runner = CliRunner()
    with patch("ai_game_studio.cli.FalFluxGenerator") as mock_generator_cls:
        mock_generator_cls.return_value.generate.return_value = generated_png

        result = runner.invoke(
            main,
            ["a brave hero", "-o", str(output_file), "--size", "64x64"],
        )

    assert result.exit_code == 0, result.output
    with Image.open(output_file) as img:
        assert img.size == (64, 64)
