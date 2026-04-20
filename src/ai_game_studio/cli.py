"""CLI entrypoints for the ai-game-studio asset generation toolchain."""

import logging
from functools import partial
from pathlib import Path

import click
from dotenv import load_dotenv

from .fal_generator import FalFluxGenerator
from .postprocess import remove_background, resize_to
from .sprite_gen import PostProcessor, generate_sprite

logger = logging.getLogger(__name__)


def _parse_size(size_str: str) -> tuple[int, int]:
    parts = size_str.lower().split("x")
    if len(parts) != 2:
        raise click.BadParameter(
            f"--size must be WxH (e.g. 64x64), got {size_str!r}"
        )
    try:
        return int(parts[0]), int(parts[1])
    except ValueError as exc:
        raise click.BadParameter(
            f"--size dimensions must be integers, got {size_str!r}"
        ) from exc


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
@click.option(
    "--size",
    default=None,
    help="Resize the generated sprite to WxH pixels (e.g. 64x64).",
)
@click.option(
    "--remove-bg",
    "remove_bg",
    is_flag=True,
    default=False,
    help="Remove the sprite background using rembg.",
)
def main(prompt: str, output: Path, size: str | None, remove_bg: bool) -> None:
    """Generate a sprite PNG from a text prompt via fal.ai FLUX.1 schnell."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    load_dotenv()

    post_processors: list[PostProcessor] = []
    if remove_bg:
        post_processors.append(remove_background)
    if size is not None:
        width, height = _parse_size(size)
        post_processors.append(partial(resize_to, width=width, height=height))

    try:
        result_path = generate_sprite(
            prompt,
            output,
            generator=FalFluxGenerator(),
            post_processors=post_processors,
        )
        click.echo(f"Generated: {result_path}")
    except Exception as exc:
        logger.exception("Sprite generation failed")
        click.echo(f"Error: {exc}", err=True)
        raise click.Abort() from exc
