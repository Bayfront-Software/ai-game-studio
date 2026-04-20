# ai-game-studio

AI-powered asset generation toolchain for indie games.

## Overview

A hub that orchestrates AI generation APIs (FLUX via fal.ai, Meshy, ElevenLabs, Suno, etc.) to produce game-ready assets: sprites, tilesets, 3D models, audio.

Built to support a 100% AI-generated pipeline where individual game projects consume this toolchain as a shared studio.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --all-extras
cp .env.example .env  # then fill in FAL_KEY
```

## Tools

- `gen-sprite "prompt"` — Generate a 2D sprite PNG via FLUX.1 schnell (fal.ai)

More generators (tileset, 3D model, audio) arrive in subsequent slices.

## Testing

```bash
uv run pytest
```

## Stack

- Python 3.12+
- uv (package manager)
- fal.ai (image generation API)
- click (CLI framework)
- pytest (testing)

## License

MIT
