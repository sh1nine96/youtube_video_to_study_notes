"""
llm.py
------
Handles all communication with the local Ollama LLM server.

Responsibilities:
  1. Send a prompt to Ollama
  2. Receive and return the response text
  3. Handle connection errors clearly
  4. Keep model config in one place

The rest of the app only needs to call: run_prompt(prompt) -> str
"""

import requests
import json

# ---------------------------------------------------------------------------
# CONFIGURATION — change model name here if you switch models later
# ---------------------------------------------------------------------------

OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "qwen2.5:7b"

# How long to wait for a response (seconds).
# Long transcripts can take 60-120 seconds to process — so we set this high.
REQUEST_TIMEOUT = 300


# ---------------------------------------------------------------------------
# CORE FUNCTION: Send a prompt, get a response
# ---------------------------------------------------------------------------

def run_prompt(prompt: str) -> str:
    """
    Send a prompt to the local Ollama LLM and return the response as a string.

    This function makes a POST request to Ollama's /api/generate endpoint.
    We use stream=False so we wait for the complete response before returning.

    Args:
        prompt: The full prompt string to send to the model.

    Returns:
        The model's response as a plain string.

    Raises:
        ConnectionError: If Ollama server is not running.
        ValueError: If the response format is unexpected.
        TimeoutError: If the model takes too long to respond.
    """

    # Build the request payload
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,      # Wait for full response, don't stream tokens
        "options": {
            "temperature": 0.3,   # Lower = more focused, less creative (good for study notes)
            "top_p": 0.9,
            "num_predict": 2048,  # Max tokens to generate per response
        }
    }

    try:
        print(f"[llm] Sending prompt to {MODEL_NAME} ({len(prompt.split())} words in prompt)...")

        response = requests.post(
            url=f"{OLLAMA_BASE_URL}/api/generate",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        # Raise an error for bad HTTP status codes (4xx, 5xx)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract the response text
        result = data.get("response", "").strip()

        if not result:
            raise ValueError("Ollama returned an empty response.")

        word_count = len(result.split())
        print(f"[llm] Response received. Words in output: {word_count}")

        return result

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Cannot connect to Ollama. Please make sure Ollama is running.\n"
            "Start it with: ollama server"
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            f"Ollama took longer than {REQUEST_TIMEOUT} seconds to respond. "
            "Try a shorter transcript or a smaller model."
        )

    except requests.exceptions.HTTPError as e:
        raise ValueError(f"Ollama server returned an error: {e}")

    except json.JSONDecodeError:
        raise ValueError("Could not parse Ollama's response as JSON.")


# ---------------------------------------------------------------------------
# HELPER: Check if Ollama is running before we start processing
# ---------------------------------------------------------------------------

def check_ollama_connection() -> bool:
    """
    Ping the Ollama server to confirm it is reachable.

    Returns:
        True if Ollama is running, False otherwise.
    """
    try:
        response = requests.get(OLLAMA_BASE_URL, timeout=5)
        return "Ollama" in response.text
    except requests.exceptions.ConnectionError:
        return False


def get_model_name() -> str:
    """Return the currently configured model name."""
    return MODEL_NAME