"""
test_llm.py
-----------
Tests llm.py and prompts.py together using a real transcript.
Runs ONE prompt (summary) to keep the test fast.
Delete after Phase 4 is confirmed working.
"""

from llm import run_prompt, check_ollama_connection, get_model_name
from prompts import build_summary_prompt
from transcript import get_transcript


def test_ollama_connection():
    """Verify Ollama is running before we try anything."""
    print("=" * 50)
    print("Test 1: Ollama Connection")
    print("=" * 50)

    if check_ollama_connection():
        print(f"  ✓ Ollama is running")
        print(f"  ✓ Model configured: {get_model_name()}")
    else:
        print("  ✗ Ollama is NOT running")
        print("  → Run: ollama serve")
        return False
    return True


def test_summary_generation():
    """Fetch a real transcript and generate a summary from it."""
    print()
    print("=" * 50)
    print("Test 2: Summary Generation (end-to-end)")
    print("=" * 50)

    # Use the same 3Blue1Brown video from Phase 3
    url = "https://www.youtube.com/watch?v=LPZh9BOjkQs"

    print(f"  Step 1: Fetching transcript from YouTube...")
    transcript, warning = get_transcript(url)
    if warning:
        print(f"  ⚠️ Warning: {warning}")
    print(f"  ✓ Transcript ready ({len(transcript.split())} words)")

    print(f"\n  Step 2: Building prompt...")
    prompt = build_summary_prompt(transcript)
    print(f"  ✓ Prompt built ({len(prompt.split())} words total)")

    print(f"\n  Step 3: Sending to {get_model_name()} (this may take 30-60 seconds)...")
    summary = run_prompt(prompt)

    print(f"\n  ✓ Summary generated!")
    print()
    print("-" * 50)
    print("GENERATED SUMMARY:")
    print("-" * 50)
    print(summary)
    print("-" * 50)


if __name__ == "__main__":
    ollama_ok = test_ollama_connection()
    if ollama_ok:
        test_summary_generation()
    print()
    print("=" * 50)
    print("If summary looks coherent and relevant, Phase 4 is complete.")
    print("=" * 50)