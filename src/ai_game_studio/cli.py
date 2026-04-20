"""CLI entrypoints for the ai-game-studio asset generation toolchain."""

import logging
from functools import partial
from pathlib import Path

import click
from dotenv import load_dotenv

from .fal_generator import FalFluxGenerator
from .postprocess import remove_background, resize_to
from .sprite_gen import PostProcessor, generate_sprite
from .spritesheet import build_spritesheet

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


@click.command(name="gen-spritesheet")
@click.argument("prompt")
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default=Path("spritesheet.png"),
    show_default=True,
    help="Output PNG file path.",
)
@click.option(
    "--frames",
    type=click.IntRange(min=1),
    default=4,
    show_default=True,
    help="Number of frames to generate.",
)
@click.option(
    "--columns",
    type=click.IntRange(min=1),
    default=2,
    show_default=True,
    help="Number of columns in the spritesheet grid.",
)
def spritesheet_main(prompt: str, output: Path, frames: int, columns: int) -> None:
    """Generate N frames of PROMPT and tile them into a spritesheet grid."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    load_dotenv()

    try:
        generator = FalFluxGenerator()
        frame_bytes = [generator.generate(prompt) for _ in range(frames)]
        sheet_bytes = build_spritesheet(frame_bytes, columns=columns)
        output.write_bytes(sheet_bytes)
        click.echo(f"Generated: {output} ({frames} frames, {columns} columns)")
    except Exception as exc:
        logger.exception("Spritesheet generation failed")
        click.echo(f"Error: {exc}", err=True)
        raise click.Abort() from exc
