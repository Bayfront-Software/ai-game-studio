"""CLI entrypoints for the ai-game-studio asset generation toolchain."""

import logging
from pathlib import Path

import click
from dotenv import load_dotenv

from .fal_generator import FalFluxGenerator
from .sprite_gen import generate_sprite

logger = logging.getLogger(__name__)


@click.command()
@click.argument("prompt")
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=Path("sprite.png"),
    show_default=True,
    help="Output PNG file path.",
)
def main(prompt: str, output: Path) -> None:
    """Generate a sprite PNG from a text prompt via fal.ai FLUX.1 schnell."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    load_dotenv()
    try:
        result_path = generate_sprite(prompt, output, generator=FalFluxGenerator())
        click.echo(f"Generated: {result_path}")
    except Exception as exc:
        logger.exception("Sprite generation failed")
        click.echo(f"Error: {exc}", err=True)
        raise click.Abort() from exc
