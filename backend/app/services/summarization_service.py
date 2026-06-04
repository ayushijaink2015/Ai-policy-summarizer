"""Summarization service using Google Gemini.

This module provides `summarize_text(text)` which:
- loads `.env` automatically (if `python-dotenv` is installed),
- reads `GEMINI_API_KEY` from the environment,
- calls the Gemini model via the `google-generativeai` SDK,
- returns a plain citizen-friendly summary (max 300 words),
- logs and returns an empty string on errors.

The implementation is written with beginner-friendly comments so
each step is easy to follow.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional, Any

try:
    # Optional helper to load a local .env file in development
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

logger = logging.getLogger(__name__)


def _load_dotenv() -> None:
    """Load a nearby `.env` file if available.

    We search parent directories for a `.env` file and load the first
    match. If `python-dotenv` is not installed we simply skip loading.
    """
    if load_dotenv is None:
        logger.debug("python-dotenv not installed; skipping .env load")
        return

    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        env_file = parent / ".env"
        if env_file.exists():
            load_dotenv(dotenv_path=env_file, override=False)
            logger.debug("Loaded .env from %s", env_file)
            return

    # fallback: let python-dotenv attempt its default search behavior
    load_dotenv(override=False)


def _get_api_key() -> Optional[str]:
    """Return the GEMINI_API_KEY from the environment, if set."""
    return os.getenv("GEMINI_API_KEY")


def summarize_text(text: str, model_name: str = "gemini-2.5-flash") -> str:
    """Generate a citizen-friendly summary for `text`.

    Returns an empty string on any error so callers can handle
    failures without exceptions.
    """
    # Load .env variables (development convenience).
    _load_dotenv()

    # Quick return for empty input.
    if not text or not text.strip():
        return ""

    # Read API key from environment.
    api_key = _get_api_key()
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment")
        return ""

    # Import the SDK lazily so the module can be imported even when
    # the dependency is not present.
    try:
        import google.generativeai as genai  # type: ignore
    except Exception:
        logger.exception("google-generativeai import failed")
        return ""

    # Configure the client if the SDK exposes a configure method.
    try:
        if hasattr(genai, "configure"):
            genai.configure(api_key=api_key)
    except Exception:
        logger.exception("Failed to configure google.generativeai client")
        return ""

    # Build the prompt for a citizen-friendly summary.
    prompt = (
        "Please write a concise, citizen-friendly summary of the text below. "
        "Use simple language, short paragraphs, and avoid jargon. "
        "Keep the summary under 300 words and include only the main facts.\n\n"
        f"Text to summarize:\n{text}"
    )

    # Call the Gemini model using the new SDK pattern.
    try:
        model = genai.GenerativeModel(model_name)
        response: Any = model.generate_content(prompt)
    except Exception:
        logger.exception("Failed to generate content from Gemini model %s", model_name)
        return ""

    # Read the generated text. The new SDK provides the final text
    # on `response.text` in many cases; handle errors gracefully.
    try:
        summary_text = response.text
    except Exception:
        logger.exception("Failed to read Gemini response text")
        return ""

    # Debugging prints preserved for local testing.
    print("Response Type:", type(response))
    print("Response Text:", getattr(response, "text", "<no text>"))

    # Trim and enforce the 300-word limit.
    summary_text = (summary_text or "").strip()
    words = summary_text.split()
    if len(words) > 300:
        summary_text = " ".join(words[:300])

    # Return only the summary text (no metadata).
    return summary_text
