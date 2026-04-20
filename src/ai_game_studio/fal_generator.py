"""fal.ai FLUX.1 schnell adapter conforming to the ImageGenerator protocol."""

import logging

import fal_client
import httpx

logger = logging.getLogger(__name__)


class FalFluxGenerator:
    MODEL_ID = "fal-ai/flux/schnell"

    def __init__(self, image_size: str = "square") -> None:
        self._image_size = image_size

    def generate(self, prompt: str) -> bytes:
        try:
            result = fal_client.subscribe(
                self.MODEL_ID,
                arguments={"prompt": prompt, "image_size": self._image_size},
            )
            image_url = result["images"][0]["url"]
            response = httpx.get(image_url)
            response.raise_for_status()
            return response.content
        except Exception:
            logger.exception("fal.ai FLUX generation failed for prompt=%r", prompt)
            raise
