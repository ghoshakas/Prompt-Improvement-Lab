

import config


class GeminiError(Exception):
    """Raised for any problem calling Gemini, with a human-readable message."""


def get_model_name() -> str:
    return config.GEMINI_MODEL


def _get_client():
    """Build a Gemini client, or raise a friendly error if the key is missing."""
    if not config.GEMINI_API_KEY:
        raise GeminiError(
            "GEMINI_API_KEY is not set. Copy backend/.env.example to "
            "backend/.env and paste in your Gemini API key."
        )
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:  # pragma: no cover - import guard
        raise GeminiError(
            "The google-genai package isn't installed. Run "
            "`pip install -r requirements.txt` in the backend folder."
        ) from exc

    http_options = types.HttpOptions(
        timeout=config.GEMINI_TIMEOUT_MS,
        retry_options=types.HttpRetryOptions(attempts=config.GEMINI_RETRIES),
    )
    return genai.Client(api_key=config.GEMINI_API_KEY, http_options=http_options)


def generate(prompt: str) -> str:
    """Send a single prompt to Gemini and return the text response."""
    client = _get_client()
    from google.genai import types

    gen_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=config.GEMINI_THINKING_BUDGET
        )
    )
    try:
        try:
            response = client.models.generate_content(
                model=config.GEMINI_MODEL, contents=prompt, config=gen_config
            )
        except TypeError:
            response = client.models.generate_content(
                model=config.GEMINI_MODEL, contents=prompt
            )
    except Exception as exc:  # the SDK raises a variety of error types
        msg = str(exc)
        if "503" in msg or "UNAVAILABLE" in msg:
            raise GeminiError(
                f"The model '{config.GEMINI_MODEL}' is busy right now "
                "(Gemini returned 'high demand'). Try again in a moment, or "
                "set a different GEMINI_MODEL in backend/.env."
            ) from exc
        raise GeminiError(f"Gemini request failed: {msg}") from exc

    text = getattr(response, "text", None)
    if not text:
        raise GeminiError(
            "Gemini returned an empty response (the content may have been "
            "blocked, or the prompt produced no text)."
        )
    return text.strip()
