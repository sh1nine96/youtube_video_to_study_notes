"""
Phase 2 smoke test.
Verifies Python environment and Ollama connection are working.
Run once, then delete.
"""

import sys
import requests


def check_python_version():
    """Confirm Python 3.11+."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 11:
        print("✓ Python version OK")
    else:
        print("✗ Please upgrade to Python 3.11+")


def check_ollama():
    """Confirm Ollama server is reachable."""
    try:
        response = requests.get("http://localhost:11434", timeout=5)
        if "Ollama" in response.text:
            print("✓ Ollama server is running")
        else:
            print("? Ollama responded but unexpectedly:", response.text)
    except requests.ConnectionError:
        print("✗ Cannot reach Ollama. Is it running?")


def check_imports():
    """Confirm all required packages are installed."""
    packages = {
        "gradio": "gradio",
        "youtube_transcript_api": "youtube-transcript-api",
        "requests": "requests",
        "dotenv": "python-dotenv",
    }
    for module, pip_name in packages.items():
        try:
            __import__(module)
            print(f"✓ {pip_name} installed")
        except ImportError:
            print(f"✗ {pip_name} NOT found — run: pip install {pip_name}")


def quick_llm_test(model: str = "qwen2.5:7b"):
    """Send one prompt to Ollama and print the response."""
    print(f"\nTesting LLM ({model})...")
    payload = {
        "model": model,
        "prompt": "Reply with exactly: SETUP COMPLETE",
        "stream": False,
    }
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=60,
        )
        data = response.json()
        reply = data.get("response", "").strip()
        print(f"Model replied: {reply}")
        print("✓ LLM is working")
    except Exception as e:
        print(f"✗ LLM test failed: {e}")


if __name__ == "__main__":
    print("=" * 40)
    print("Phase 2 Setup Verification")
    print("=" * 40)

    check_python_version()
    print()
    check_imports()
    print()
    check_ollama()
    print()

    # Change "llama3.2:3b" to "qwen2.5:7b" if that's what you pulled
    quick_llm_test(model="qwen2.5:7b")

    print()
    print("=" * 40)
    print("If all items show ✓, Phase 2 is complete.")
    print("=" * 40)