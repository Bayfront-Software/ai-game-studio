"""Tests for the fal.ai FLUX adapter."""

from unittest.mock import MagicMock, patch

from ai_game_studio.fal_generator import FalFluxGenerator


def test_fal_flux_generator_returns_bytes_downloaded_from_response_url() -> None:
    fake_url = "https://fal.ai/fake.png"
    fake_bytes = b"real-png-data"

    fake_response = MagicMock()
    fake_response.content = fake_bytes

    subscribe_patch = patch(
        "ai_game_studio.fal_generator.fal_client.subscribe",
        return_value={"images": [{"url": fake_url}]},
    )
    get_patch = patch(
        "ai_game_studio.fal_generator.httpx.get",
        return_value=fake_response,
    )

    with subscribe_patch, get_patch as mock_get:
        result = FalFluxGenerator().generate("pixel art hero")

    assert result == fake_bytes
    mock_get.assert_called_once_with(fake_url)


def test_fal_flux_generator_forwards_prompt_and_model_id_to_fal_client() -> None:
    fake_response = MagicMock()
    fake_response.content = b""

    subscribe_patch = patch(
        "ai_game_studio.fal_generator.fal_client.subscribe",
        return_value={"images": [{"url": "https://fal.ai/x.png"}]},
    )
    get_patch = patch(
        "ai_game_studio.fal_generator.httpx.get",
        return_value=fake_response,
    )

    with subscribe_patch as mock_subscribe, get_patch:
        FalFluxGenerator().generate("dark cozy witch")

    mock_subscribe.assert_called_once()
    (model_id,), kwargs = mock_subscribe.call_args
    assert model_id == "fal-ai/flux/schnell"
    assert kwargs["arguments"]["prompt"] == "dark cozy witch"


