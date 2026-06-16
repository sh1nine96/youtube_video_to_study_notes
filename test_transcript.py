""" test_transcript.py
------------------
Tests transcript.py with real YouTube URLs.
Run this file directly to verify the module works.
Delete after Phase 3 is confirmed working.
"""

from transcript import extract_video_id, get_transcript


def test_video_id_extraction():
    """Test that all URL formats return the correct video ID."""

    print("=" * 50)
    print("Test 1: Video ID Extraction")
    print("=" * 50)

    # All these should return the same video ID
    test_cases = {
        "Standard URL":  "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "Short URL":     "https://youtu.be/dQw4w9WgXcQ",
        "With timestamp":"https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s",
        "Embed URL":     "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "Mobile URL":    "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
    }

    expected_id = "dQw4w9WgXcQ"

    for name, url in test_cases.items():
        try:
            video_id = extract_video_id(url)
            status = "✓" if video_id == expected_id else "✗ WRONG"
            print(f"  {status}  {name}: {video_id}")
        except ValueError as e:
            print(f"  ✗  {name}: ERROR — {e}")


def test_real_transcript():
    """Fetch and display the first 300 words of a real transcript."""

    print()
    print("=" * 50)
    print("Test 2: Real Transcript Fetch")
    print("=" * 50)

    # A short, educational YouTube video with reliable English captions.
    # "How does the stock market work?" by TED-Ed (~5 min)
    test_url = "https://www.youtube.com/watch?v=zxVoCw3P1Gc"

    print(f"  URL: {test_url}")
    print("  Fetching transcript (requires internet)...\n")

    try:
        transcript = get_transcript(test_url)

        word_count = len(transcript.split())
        print(f"  ✓ Transcript fetched successfully")
        print(f"  ✓ Total words: {word_count}")
        print()
        print("  First 300 words:")
        print("-" * 50)
        preview = " ".join(transcript.split()[:3000])
        print(preview)
        print("-" * 50)

    except ValueError as e:
        print(f"  ✗ Error: {e}")


if __name__ == "__main__":
    test_video_id_extraction()
    test_real_transcript()