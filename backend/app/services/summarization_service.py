"""Summarization service using Google Gemini.

This module loads environment settings from a `.env` file and
provides a single `summarize_text` function.
The function uses the `google-generativeai` package and reads
`GEMINI_API_KEY` so secrets stay out of the source code.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

logger = logging.getLogger(__name__)


def _load_dotenv() -> None:
    """Load the `.env` file from the repository root.

    If `python-dotenv` is not available, this function logs a warning
    and continues without failing.
    """
    if load_dotenv is None:
        logger.warning(
            "python-dotenv is not installed, skipping .env loading. "
            "Set GEMINI_API_KEY directly in the environment."
        )
        return

    # Determine the repository root relative to this file.
    repo_root = Path(__file__).resolve().parents[4]
    env_path = repo_root / ".env"

    # If the `.env` file exists at the repo root, load it. If it does not
    # exist, fall back to the default search behavior of python-dotenv.
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
    else:
        load_dotenv(override=False)


def _get_api_key() -> Optional[str]:
    """Return the GEMINI_API_KEY from the environment."""
    return os.getenv("GEMINI_API_KEY")


def summarize_text(text: str, model_name: str = "gemini-2.5-flash") -> str:
    """Generate a citizen-friendly summary for `text`.

    Args:
        text: The input text to summarize.
        model_name: The Gemini model name to use.

    Returns:
        A summary string with at most 300 words. If the API fails or the
        input is invalid, this returns an empty string.
    """
    # Load .env variables before reading the API key.
    _load_dotenv()

    # If there is no text, return an empty string right away.
    if not text or not text.strip():
        return ""

    # Read the API key from the environment now that dotenv is loaded.
    api_key = _get_api_key()
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in the environment.")
        return ""

    # Import the Google generative AI library at runtime so the module
    # still loads even if the package is missing.
    try:
        import google.generativeai as genai  # type: ignore
    except Exception:
        logger.exception("Failed to import google.generativeai package.")
        return ""

    # Configure the library with the API key. This allows the package to
    # authenticate requests to the Gemini API.
    try:
        if hasattr(genai, "configure"):
            genai.configure(api_key=api_key)
    except Exception:
        logger.exception("Failed to configure google.generativeai client.")
        return ""

    # Build an explicit prompt for a citizen-friendly summary.
    # The prompt asks for simple language and a maximum of 300 words.
    prompt = (
        "Please write a concise, citizen-friendly summary of the text below. "
        "Use simple language, short paragraphs, and avoid jargon. "
        "Keep the summary under 300 words and include only the main facts.\n\n"
        f"Text to summarize:\n{text}"
    )

    try:
        # Create the new Gemini model object and generate content.
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
    except Exception:
        logger.exception("Failed to call the Gemini model.")
        return ""
       

    try:
        summary_text = response.text
    except Exception:
        logger.exception("Failed to read Gemini response.")
        return ""

   
    summary_text = summary_text.strip()

    words = summary_text.split()
    if len(words) > 300:
        summary_text = " ".join(words[:300])

    return summary_text
