"""
app.py
------
Main Gradio application for YouTube Video to Study Notes.

Milestone 6.3: Final tabbed layout — each output type gets its own
dedicated tab instead of one long scrolling page.
"""

import gradio as gr
from transcript import get_transcript
from study_generator import generate_all_study_material_stream


def process_video(url: str):
    """
    Full pipeline: URL -> transcript -> all 5 study outputs.

    Generator function — yields updates to ALL 6 output components
    (1 status box + 5 tab contents) on every step, so Gradio can
    update the UI live as each section completes.

    Yields:
        A tuple of 6 values matching the 6 outputs wired to this
        function: (status, summary, study_notes, key_concepts, mcqs, interview_qs)
    """

    # Initial empty state for all 5 content tabs
    empty = "*Waiting for processing to start...*"

    if not url or not url.strip():
        yield "⚠️ Please enter a YouTube URL.", empty, empty, empty, empty, empty
        return

    # --- Step 1: Fetch transcript ---
    yield "🔄 Step 1/2: Fetching transcript from YouTube...", empty, empty, empty, empty, empty

    try:
        transcript = get_transcript(url)
    except ValueError as e:
        error_msg = f"❌ Error fetching transcript:\n\n{str(e)}"
        yield error_msg, empty, empty, empty, empty, empty
        return

    word_count = len(transcript.split())
    status = f"✓ Transcript fetched ({word_count} words). Generating study material..."
    yield status, empty, empty, empty, empty, empty

    # --- Step 2: Stream live progress through all 5 generation steps ---
    # We keep a running dict of whatever has been generated so far, so that
    # completed tabs display their content immediately instead of waiting
    # for ALL 5 to finish.
    current_results = {
        "summary": empty,
        "study_notes": empty,
        "key_concepts": empty,
        "mcqs": empty,
        "interview_questions": empty,
    }

    for status_message, results in generate_all_study_material_stream(transcript):
        if results is None:
            # Still processing — update status only, tabs show what's done so far
            live_status = f"✓ Transcript fetched ({word_count} words)\n\n🔄 {status_message}"
            yield (
                live_status,
                current_results["summary"],
                current_results["study_notes"],
                current_results["key_concepts"],
                current_results["mcqs"],
                current_results["interview_questions"],
            )
        else:
            # Final batch — all 5 are done, update everything at once
            current_results = results
            final_status = "✅ All study material generated successfully!"
            yield (
                final_status,
                current_results.get("summary", "Not available"),
                current_results.get("study_notes", "Not available"),
                current_results.get("key_concepts", "Not available"),
                current_results.get("mcqs", "Not available"),
                current_results.get("interview_questions", "Not available"),
            )


# ---------------------------------------------------------------------------
# Build the UI
# ---------------------------------------------------------------------------

with gr.Blocks(title="YouTube Study Notes Generator") as demo:

    gr.Markdown("# 📚 YouTube Video to Study Notes")
    gr.Markdown("Paste a YouTube URL below and generate study material instantly.")

    with gr.Row():
        url_input = gr.Textbox(
            label="YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            scale=4,
        )
        generate_btn = gr.Button("Generate", variant="primary", scale=1)

    status_display = gr.Markdown("*Enter a URL and click Generate to begin.*")

    with gr.Tabs():
        with gr.Tab("📝 Summary"):
            summary_output = gr.Markdown()

        with gr.Tab("📚 Study Notes"):
            study_notes_output = gr.Markdown()

        with gr.Tab("🔑 Key Concepts"):
            key_concepts_output = gr.Markdown()

        with gr.Tab("❓ MCQs"):
            mcqs_output = gr.Markdown()

        with gr.Tab("💼 Interview Questions"):
            interview_output = gr.Markdown()

    generate_btn.click(
        fn=process_video,
        inputs=url_input,
        outputs=[
            status_display,
            summary_output,
            study_notes_output,
            key_concepts_output,
            mcqs_output,
            interview_output,
        ],
    )


if __name__ == "__main__":
    demo.launch()