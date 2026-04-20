"""End-to-end tests for the gen-sprite CLI command."""

from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from PIL import Image

from ai_game_studio.cli import main, spritesheet_main


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


def test_cli_removes_background_when_flag_given(tmp_path: Path) -> None:
    output_file = tmp_path / "hero.png"
    raw_bytes = b"raw-from-fal"
    bg_removed_bytes = b"transparent-result"

    runner = CliRunner()
    generator_patch = patch("ai_game_studio.cli.FalFluxGenerator")
    remove_bg_patch = patch(
        "ai_game_studio.cli.remove_background",
        return_value=bg_removed_bytes,
    )
    with generator_patch as mock_gen_cls, remove_bg_patch as mock_remove:
        mock_gen_cls.return_value.generate.return_value = raw_bytes

        result = runner.invoke(
            main,
            ["a hero", "-o", str(output_file), "--remove-bg"],
        )

    assert result.exit_code == 0, result.output
    mock_remove.assert_called_once_with(raw_bytes)
    assert output_file.read_bytes() == bg_removed_bytes


def test_spritesheet_cli_generates_frames_and_tiles_them_into_grid(
    tmp_path: Path,
) -> None:
    output_file = tmp_path / "sheet.png"
    frame_png = _make_solid_png(16, 16)

    runner = CliRunner()
    with patch("ai_game_studio.cli.FalFluxGenerator") as mock_generator_cls:
        mock_generator_cls.return_value.generate.return_value = frame_png

        result = runner.invoke(
            spritesheet_main,
            ["a hero", "-o", str(output_file), "--frames", "4", "--columns", "2"],
        )

    assert result.exit_code == 0, result.output
    assert mock_generator_cls.return_value.generate.call_count == 4
    with Image.open(output_file) as sheet:
        assert sheet.size == (32, 32)
