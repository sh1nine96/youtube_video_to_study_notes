"""
test_study_generator.py
------------------------
Full end-to-end test: URL -> transcript -> all 5 study outputs.
This is the most important test in the whole project so far.
Delete after Phase 5 is confirmed working.
"""

from transcript import get_transcript
from study_generator import generate_all_study_material, format_results_as_markdown


def main():
    print("=" * 60)
    print("FULL PIPELINE TEST: URL -> Transcript -> Study Material")
    print("=" * 60)

    url = "https://www.youtube.com/watch?v=rEDzUT3ymw4"

    print(f"\nStep 1: Fetching transcript...")
    transcript = get_transcript(url)
    print(f"✓ Transcript ready ({len(transcript.split())} words)")

    print(f"\nStep 2: Generating all study material (this takes a few minutes)...")
    results = generate_all_study_material(transcript)

    print("\n" + "=" * 60)
    print("ALL RESULTS")
    print("=" * 60)

    for key in ["summary", "study_notes", "key_concepts", "mcqs", "interview_questions"]:
        content = results.get(key, "MISSING")
        word_count = len(content.split())
        print(f"\n--- {key.upper()} ({word_count} words) ---")
        print(content[:700])  # print first 500 chars only, to keep terminal readable
        print("..." if len(content) > 700 else "")

    # Save the full output to a file so you can review everything properly
    full_markdown = format_results_as_markdown(results)
    with open("test_output.md", "w", encoding="utf-8") as f:
        f.write(full_markdown)

    print("\n" + "=" * 60)
    print("✓ Full output saved to test_output.md")
    print("  Open it in VS Code to review everything properly.")
    print("=" * 60)


if __name__ == "__main__":
    main()