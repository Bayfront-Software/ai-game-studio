"""End-to-end tests for the gen-sprite CLI command."""

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from ai_game_studio.cli import main


def test_cli_invokes_generator_and_writes_sprite_to_output_path(tmp_path: Path) -> None:
    output_file = tmp_path / "hero.png"
    fake_bytes = b"cli-test-bytes"

    runner = CliRunner()
    with patch("ai_game_studio.cli.FalFluxGenerator") as mock_generator_cls:
        mock_generator_cls.return_value.generate.return_value = fake_bytes

        result = runner.invoke(main, ["a brave hero", "-o", str(output_file)])

    assert result.exit_code == 0, result.output
    assert output_file.read_bytes() == fake_bytes
